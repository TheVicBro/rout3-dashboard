<script lang="ts">
  import { createQuery, useQueryClient } from '@tanstack/svelte-query';
  import { writable, get } from 'svelte/store';
  import { DateTime } from 'luxon';
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";
  import * as Command from "$lib/components/ui/command/index.js";
  import * as Popover from "$lib/components/ui/popover/index.js";
  import { Input } from "$lib/components/ui/input/index.js";
  import { Button } from "$lib/components/ui/button/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import { Slider } from "$lib/components/ui/slider/index.js";
  import { cn } from "$lib/utils.js";
  import { CirclePlus, Check, ChevronsUpDown } from "lucide-svelte";
  import { availableModelProviders, closeAndFocusTrigger } from "../utils/utils"; 
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
    const response = await fetch(`http://127.0.0.1:8000/api/v1/config/model/${config?.id}`, {
      method: 'GET',
      headers: {
        'accept': 'application/json',
      }
    });
    const data = await response.json();
    return z.array(ModelConfigSchema).parse(data);
  }

  const fetchSecrets = async (): Promise<Secret[]> => {
    const response = await fetch(`http://127.0.0.1:8000/api/v1/secrets`, {
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
    const response = await fetch('http://127.0.0.1:8000/api/v1/config/', {
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
    const response = await fetch('http://127.0.0.1:8000/api/v1/config/', {
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
      const response = await fetch(`http://127.0.0.1:8000/api/v1/config/model?secret_id=${selectedSecret?.id}`, {
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

  const modelConfigQuery = createQuery<ModelConfig[]>({
    queryKey: ['apiData'],
    queryFn: fetchModelConfig,
  });

  const secretQuery = createQuery<Secret[]>({
    queryKey: ['secretData'],
    queryFn: fetchSecrets,
  });

  let open = false;
  $: selectedValue = selectedSecret?.name || "Select a secret...";
  let selectedSecret: Secret | null = null;
</script>

<div class="flex flex-col h-screen">
  <Toaster />
  <h1 class="p-8 pl-20 text-3xl font-bold bg-white dark:bg-slate-900 border-b-2 dark:border-black">Configuration</h1>
  <div class="flex-1 overflow-auto">
    <div class="m-10 border dark:border-black rounded-lg bg-white dark:bg-slate-900 shadow">
      <h2 class="p-10 pb-4 leading-none text-2xl font-semibold border-b-2 dark:border-black">Overview</h2>
      <div class="p-20 px-64">
        <h3 class="text-xl font-semibold mb-2">Currently Selected Models</h3>
        {#if $modelConfigQuery.isPending}
          <Skeleton />
        {:else if $modelConfigQuery.error}
          <p class="text-red-600">An error has occurred: {$modelConfigQuery.error.message}</p>
        {:else if $modelConfigQuery.data.length === 0}
          <div class="flex flex-col items-center">
            <CirclePlus class="w-12 h-12 mb-4 text-gray-400" />
            <p>No Models added yet. Click "Add model" to add a new model.</p>
          </div>
        {:else}
          <table class="w-full">
            <tbody>
              {#each $modelConfigQuery.data as model}
                <tr>
                  <td class="p-2 flex items-center gap-x-2">{model.model}<p class="text-xs text-gray-400">(ID: {model.id})</p></td>
                </tr>
              {/each}
            </tbody>
          </table>
        {/if}
        <h3 class="text-xl font-semibold mt-8 mb-2">Select a Provider Secret</h3>
        <Popover.Root bind:open let:ids>
          <Popover.Trigger asChild let:builder>
            <Button
              builders={[builder]}
              variant="outline"
              role="combobox"
              aria-expanded={open}
              class="w-[200px] justify-between"
            >
              {selectedValue}
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

        <h3 class="text-xl font-semibold my-4">Model Settings</h3>
        <div class="mb-4">
          <Label for="modelName" class="block font-semibold mb-1">Model Name</Label>
          <Input id="modelName" bind:value={modelName} class="mt-4" />
        </div>
        <div class="mb-4">
          <Label for="temperature">Temperature: {temperature[0].toFixed(2)}</Label>
          <Slider id="temperature" bind:value={temperature} min={0} max={1} step={0.01} class="mt-4" />
        </div>
        <div class="mb-4">
          <Label for="maxTokens" class="block font-semibold mb-1">Max Tokens</Label>
          <Input id="maxTokens" type="number" min="1" max="1000" bind:value={$maxTokens} class="mt-2" />
        </div>
        <div>
          <Button on:click={addModel} class="px-4 py-2 text-white rounded-lg bg-blue-800 hover:bg-blue-700 transition">Add Model</Button>
        </div>
      </div>
    </div>
  </div>
</div>
