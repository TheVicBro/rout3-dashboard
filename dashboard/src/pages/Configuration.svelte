<script lang="ts">
  import { createQuery, useQueryClient } from '@tanstack/svelte-query';
  import { writable, get } from 'svelte/store';
  import { DateTime } from 'luxon';
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";
  import { Dialog as DialogPrimitive } from "bits-ui";
  import * as Dialog from "$lib/components/ui/dialog";
  import * as Command from "$lib/components/ui/command/index.js";
  import * as Popover from "$lib/components/ui/popover/index.js";
  import { Input } from "$lib/components/ui/input/index.js";
  import { Button } from "$lib/components/ui/button/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import { Slider } from "$lib/components/ui/slider/index.js";
  import { cn } from "$lib/utils.js";
  import { CirclePlus, Check, ChevronsUpDown } from "lucide-svelte";
  import { closeAndFocusTrigger } from "../utils/utils"; 
	import { onMount } from 'svelte';
  import Skeleton from "../components/Skeleton.svelte"
  import { z } from 'zod';

  let temperature = [0.7];
  let config: Config | null = null;
  let modelName = '';
  const maxTokens = writable(100);
  const token = localStorage.getItem("authToken");
  const queryClient = useQueryClient();

  interface Config {
    timeout: number;
    route_type: string;
    id: number;
    router_name: string;
    user_id: number;
  }

  const ModelConfigSchema = z.object({
    model: z.string(),
    max_tokens: z.number(),
    temperature: z.number(),
    id: z.number(),
    config_id: z.number(),
  });

  const SecretSchema = z.object({
    name: z.string(),
    last_used: z.string().nullable(),
    user_id: z.number(),
    id: z.number(),
  });

  type ModelConfig = z.infer<typeof ModelConfigSchema>;
  type Secret = z.infer<typeof SecretSchema>;

  onMount(async () => {
    if (config) {
      toast.success('Configuration already loaded');
    } else {
      try {
        config = await getConfig();
        toast.success('Configuration loaded successfully');
      } catch (error) {
        toast.error('Failed to fetch config', {
          description: 'Attempting to create new config...',
        });
        try {
          config = await createConfig({
            timeout: 30, // default value
            route_type: "cost" // default value
          });
          toast.success('New configuration created successfully');
        } catch (createError) {
          toast.error('Error creating new config', {
            description: createError instanceof Error ? createError.message : 'Unknown error',
          });
        }
      }
    }
  });

  async function fetchModelConfig(): Promise<ModelConfig[]> {
    const response = await fetch(`https://rout3-backend.vercel.app/api/v1/config/model/${config?.id}`, {
      method: 'GET',
      headers: {
        'accept': 'application/json',
      }
    });
    const data = await response.json();
    return z.array(ModelConfigSchema).parse(data);
  }

  const fetchSecrets = async (): Promise<Secret[]> => {
    const response = await fetch(`https://rout3-backend.vercel.app/api/v1/secrets`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      }
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Network response was not ok: ${response.statusText}`);
    }
    const data = await response.json();
    return z.array(SecretSchema).parse(data);
  };

  async function getConfig(): Promise<Config> {
    const response = await fetch('https://rout3-backend.vercel.app/api/v1/config/', {
      method: 'GET',
      headers: {
        'accept': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  async function createConfig(newConfig: { timeout: number; route_type: string }): Promise<Config> {
    const response = await fetch('https://rout3-backend.vercel.app/api/v1/config/', {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(newConfig)
    });

    if (!response.ok) {
      if (response.status === 422) {
        const errorData = await response.json();
        throw new Error(`Validation Error: ${JSON.stringify(errorData.detail)}`);
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  const addModel = async () => {
    const maxTokenCount = get(maxTokens);
    const current_date = DateTime.now();
    const formatted_date = current_date.toFormat('yyyy-MM-dd HH:mm:ss');

    try {
      const response = await fetch(`https://rout3-backend.vercel.app/api/v1/config/model?secret_id=${selectedSecret?.id}`, {
        method: 'POST',
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          model: modelName,
          max_tokens: maxTokenCount,
          temperature: temperature[0],
        })
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Network response was not ok: ${response.statusText}`);
      }
      await queryClient.invalidateQueries({ queryKey: ['apiData'] });
      toast.success(`${modelName} has been added.`, {
        description: `${formatted_date}`,
      })
      modelName = '';
    } catch (error) {
      toast.error('Failed to add model', {
        description: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  const removeModel = async () => {
    const current_date = DateTime.now();
    const formatted_date = current_date.toFormat('yyyy-MM-dd HH:mm:ss');
    modelName = selectedModel?.model || '';

    try {
      const response = await fetch(`https://rout3-backend.vercel.app/api/v1/config/model/${selectedModel?.id}`, {
        method: 'DELETE',
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Network response was not ok: ${response.statusText}`);
      }
      await queryClient.invalidateQueries({ queryKey: ['apiData'] });
      toast.success(`${modelName} has been removed.`, {
        description: `${formatted_date}`,
      })
      modelName = '';
    } catch (error) {
      toast.error('Failed to remove model', {
        description: error instanceof Error ? error.message : 'Unknown error',
      });
    }
  }

  const modelConfigQuery = createQuery<ModelConfig[]>({
    queryKey: ['apiData'],
    queryFn: fetchModelConfig,
  });

  const secretQuery = createQuery<Secret[]>({
    queryKey: ['secretData'],
    queryFn: fetchSecrets,
  });

  let open = false;
  let addDialogOpen = false;
  let removeDialogOpen = false;
  $: selectedAddValue = selectedSecret?.name || "Select a secret...";
  $: selectedRemoveValue = selectedModel?.model || "Select a model...";
  let selectedSecret: Secret | null = null;
  let selectedModel: ModelConfig | null = null;
</script>

<div class="flex flex-col h-screen">
  <Toaster />
  <h1 class="p-8 pl-20 text-3xl font-bold bg-white dark:bg-slate-900 border-b-2 dark:border-black">Configuration</h1>
  <div class="flex-1 overflow-auto">
    <div class="m-10 border dark:border-black rounded-lg bg-white dark:bg-slate-900 shadow">
      <h2 class="p-10 pb-4 leading-none text-2xl font-semibold border-b-2 dark:border-black">Overview</h2>
      <div class="p-20 px-64">
        {#if $modelConfigQuery.isPending || $modelConfigQuery.error}
          <Skeleton />
        {:else if $modelConfigQuery.data.length === 0}
          <div class="flex flex-col items-center">
            <CirclePlus class="w-12 h-12 mb-4 text-gray-400" />
            <p>No Models added yet. Click "Add model" to add a new model.</p>
          </div>
        {:else}
          <h3 class="text-xl font-semibold mb-2">Currently Selected Models</h3>
          <div class="flex flex-wrap gap-4 mt-8">
            {#each $modelConfigQuery.data as model}
              {#if model && model.model}
                <div class="flex items-center justify-center px-4 py-2 border-2 border-gray-300 rounded-full hover:border-blue-500 transition-colors cursor:pointer">
                  <span class="font-medium select-none">{model.model}</span>
                  <span class="ml-2 text-xs text-gray-400 select-none">(ID: {model.id})</span>
                </div>
              {:else}
                <div class="flex items-center justify-center px-4 py-2 border-2 border-gray-300 rounded-full">
                  <span class="font-medium select-none">Loading...</span>
                </div>
              {/if}
            {/each}
          </div>
        {/if}
      </div>
    </div>

    <!-- Add Model Dialog -->
    <Dialog.Root bind:open={addDialogOpen}>
      <Dialog.Trigger>
        <Button class="ml-10 px-8 py-2 bg-blue-800 transition hover:bg-blue-700 hover:transition text-white rounded-lg">Add Model</Button>
      </Dialog.Trigger>
      <Dialog.Content>
        <Dialog.Header>
          <Dialog.Title>Add Model</Dialog.Title>
          <Dialog.Description>
            Fill in the details below to add a new model.
          </Dialog.Description>
          <h3 class="text-lg font-semibold mt-8 mb-2">Select a Provider Secret</h3>
          <Popover.Root bind:open let:ids>
            <Popover.Trigger asChild let:builder>
              <Button
                builders={[builder]}
                variant="outline"
                role="combobox"
                aria-expanded={open}
                class="w-[200px] justify-between"
              >
                {selectedAddValue}
                <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
              </Button>
            </Popover.Trigger>
            <Popover.Content class="w-[200px] p-0">
              <Command.Root>
                <Command.Input placeholder="Search provider..." />
                <Command.Empty>No provider found.</Command.Empty>
                <Command.Group>
                  {#if $secretQuery.isPending}
                    <Command.Item>Loading secrets...</Command.Item>
                  {:else if $secretQuery.error}
                    <Command.Item>Error loading secrets: {$secretQuery.error.message}</Command.Item>
                  {:else if $secretQuery.data.length === 0}
                    <Command.Item>No secrets available</Command.Item>
                  {:else}
                    {#each $secretQuery.data as secret}
                      <Command.Item
                        value={secret.name}
                        onSelect={() => {
                          selectedSecret = secret;
                          closeAndFocusTrigger(ids.trigger);
                          open = false;
                        }}
                      >
                        <Check
                          class={cn(
                            "mr-2 h-4 w-4",
                            selectedSecret?.id !== secret.id && "text-transparent"
                          )}
                        />
                        {secret.name} (ID: {secret.id})
                      </Command.Item>
                    {/each}
                  {/if}
                </Command.Group>
              </Command.Root>
            </Popover.Content>
          </Popover.Root>
          <div class="grid gap-4 py-4">
            <h3 class="text-lg font-semibold">Model Settings</h3>
            <div class="grid grid-cols-5 items-center gap-4">
              <Label for="modelName" class="text-center">Model Name</Label>
              <Input id="modelName" bind:value={modelName} class="col-span-4" />
            </div>
            <div class="grid grid-cols-5 items-center gap-4">
              <Label for="temperature" class="text-center text-sm">Temperature: {temperature[0].toFixed(2)}</Label>
              <Slider id="temperature" bind:value={temperature} min={0} max={1} step={0.01} class="col-span-4" />
            </div>
            <div class="grid grid-cols-5 items-center gap-4">
              <Label for="maxTokens" class="text-center">Max Tokens</Label>
              <Input id="maxTokens" type="number" min="1" max="1000" bind:value={$maxTokens} class="col-span-4" />
            </div>
          </div>
          <Dialog.Footer>
            <DialogPrimitive.Close>
              <Button on:click={addModel} class="px-4 py-2 text-white rounded-lg bg-blue-800 hover:bg-blue-700 transition">Add Model</Button>
            </DialogPrimitive.Close>
          </Dialog.Footer>
        </Dialog.Header>
      </Dialog.Content>
    </Dialog.Root>

    <!-- Remove Model Dialog -->
    <Dialog.Root bind:open={removeDialogOpen}>
      <Dialog.Trigger>
        <Button class="ml-10 px-8 py-2 bg-red-800 transition hover:bg-red-700 hover:transition text-white rounded-lg">Remove Model</Button>
      </Dialog.Trigger>
      <Dialog.Content>
        <Dialog.Header>
          <Dialog.Title>Remove Model</Dialog.Title>
          <Dialog.Description>
            Select a model to remove.
          </Dialog.Description>
          <Popover.Root bind:open let:ids>
            <Popover.Trigger asChild let:builder>
              <Button
                builders={[builder]}
                variant="outline"
                role="combobox"
                aria-expanded={open}
                class="w-[200px] justify-between"
              >
                {selectedRemoveValue}
                <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
              </Button>
            </Popover.Trigger>
            <Popover.Content class="w-[200px] p-0">
              <Command.Root>
                <Command.Input placeholder="Search provider..." />
                <Command.Empty>No provider found.</Command.Empty>
                <Command.Group>
                  {#if $modelConfigQuery.isPending}
                    <Command.Item>Loading models...</Command.Item>
                  {:else if $modelConfigQuery.error}
                    <Command.Item>Error loading models: {$modelConfigQuery.error.message}</Command.Item>
                  {:else if $modelConfigQuery.data.length === 0}
                    <Command.Item>No models available</Command.Item>
                  {:else}
                    {#each $modelConfigQuery.data as models}
                      <Command.Item
                        value={models.model}
                        onSelect={() => {
                          selectedModel = models;
                          closeAndFocusTrigger(ids.trigger);
                          open = false;
                        }}
                      >
                        <Check
                          class={cn(
                            "mr-2 h-4 w-4",
                            selectedModel?.id !== models.id && "text-transparent"
                          )}
                        />
                        {models.model} (ID: {models.id})
                      </Command.Item>
                    {/each}
                  {/if}
                </Command.Group>
              </Command.Root>
            </Popover.Content>
          </Popover.Root>
          <Dialog.Footer>
            <DialogPrimitive.Close>
              <Button on:click={removeModel} class="px-4 py-2 text-white rounded-lg bg-red-800 hover:bg-red-700 transition">Remove Model</Button>
            </DialogPrimitive.Close>
          </Dialog.Footer>
        </Dialog.Header>
      </Dialog.Content>
    </Dialog.Root>
  </div>
</div>
