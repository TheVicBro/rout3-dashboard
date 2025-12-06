<script lang="ts">
  import { createQuery, useQueryClient } from '@tanstack/svelte-query';
  import { DateTime } from 'luxon';
  import { Input } from "$lib/components/ui/input/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import { Dialog as DialogPrimitive } from "bits-ui";
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";
  import { Button } from "$lib/components/ui/button/index.js";
  import { cn } from "$lib/utils.js";
  import { z } from 'zod';
  import { CirclePlus, Check, ChevronsUpDown } from "lucide-svelte";
  import { closeAndFocusTrigger } from "$lib/utils"; 
  import { isAuthenticated } from '../stores/auth';
  import { navigate } from 'svelte-routing';
  import * as Dialog from "$lib/components/ui/dialog";
  import * as Command from "$lib/components/ui/command/index.js";
  import * as Popover from "$lib/components/ui/popover/index.js";
  import Skeleton from "../components/Skeleton.svelte"
  import { api } from "$lib/api";

  const queryClient = useQueryClient();

  const APISchema = z.object({
    name: z.string(),
    id: z.number(),
    user_id: z.number(),
  });

  const APIOptionSchema = z.object({
    id: z.number(),
    name: z.string(),
  });

  type API = z.infer<typeof APISchema>;
  type SelectedAPIOption = z.infer<typeof APIOptionSchema>;

  let selectedAPItoDelete: SelectedAPIOption | null = null;
  let newName = '';
  let open = false;

  const createAPI = async () => {
    creatingAPI = true;
    const current_date = DateTime.now();
    const formatted_date = current_date.toFormat('yyyy-MM-dd HH:mm:ss');

    try {
      const data = await api.post<{ key: string }>('/myapi', { name: newName });
      newApiKey = data.key;
      await queryClient.invalidateQueries({ queryKey: ['apiData'] });
      toast.success(`${newName} has been added.`, {
        description: `${formatted_date}`,
      })
      apiCreationSuccess = true;
    } catch (error) {
      if (error instanceof z.ZodError) {
        toast.error("Validation error", {
          description: error.errors.map(e => e.message).join(", ")
        });
      } else {
        toast.error("An error occurred", {
          description: error instanceof Error ? error.message : "Unknown error"
        });
      }
    }
    creatingAPI = false;
  }

  const deleteAPI = async () => {
    const formatted_date = DateTime.now().toFormat('yyyy-MM-dd HH:mm:ss');

    if (!selectedAPItoDelete) {
        throw new Error('No API selected for removal');
      }

    try {
      const validatedAPI = APIOptionSchema.parse(selectedAPItoDelete);
      await api.delete(`/myapi/${validatedAPI.id}`);

      await queryClient.invalidateQueries({ queryKey: ['apiData'] });
      toast.success(`${selectedAPItoDelete.name} has been removed.`, {
        description: `${formatted_date}`,
      });
      selectedAPItoDelete = null;
    } catch (error) {
      toast.error("An error occurred", {
        description: error instanceof Error ? error.message : "Unknown error"
      });
    }
  }

  const fetchAPI = async (): Promise<API[]> => {
    const data = await api.get<unknown>('/myapi');
    return z.array(APISchema).parse(data);
  };

  const query = createQuery<API[]>({
    queryKey: ['apiData'],
    queryFn: fetchAPI,
  });

  $: selectedRemoveValue = selectedAPItoDelete 
    ? `${selectedAPItoDelete.name} (ID: ${selectedAPItoDelete.id})` 
    : "Select a key to remove...";

  let apiCreationSuccess = false;
  let dialogOpen = false;
  let newApiKey = '';
  let copiedText = 'Copy';
  let creatingAPI = false;

  const handleDialogClose = () => {
    dialogOpen = false;
    apiCreationSuccess = false;
    newName = '';
    newApiKey = '';
    copiedText = 'Copy';
  }

  $: if (!dialogOpen) {
    handleDialogClose();
  }

  const copyToClipboard = () => {
    navigator.clipboard.writeText(newApiKey);
    copiedText = 'Copied!';
    setTimeout(() => {
      copiedText = 'Copy';
    }, 2000);
  }
</script>

<div>
  <Toaster />
  <h1 class="p-8 pl-20 text-3xl font-bold bg-white dark:bg-slate-900 border-b-2 dark:border-black">MyAPI</h1>
  <div class="m-10 border dark:border-black rounded-lg bg-white dark:bg-slate-900 shadow">
    <h2 class="p-10 pb-4 leading-none text-2xl font-semibold border-b-2 dark:border-black">Overview</h2>
    <div class="p-10">
      {#if $query.isPending || $query.error}
        <Skeleton />
      {:else if $query.data.length === 0}
        <div class="flex flex-col items-center">
          <CirclePlus class="w-12 h-12 mb-4 text-gray-400" />
          <p>No APIs found. Click "Create API" to add a new API.</p>
        </div>
      {:else}
        <table class="w-full">
          <thead>
            <tr>
              <th class="text-left p-2">Name</th>
              <th class="text-left p-2">Key</th>
            </tr>
          </thead>
          <tbody>
            {#each $query.data as api}
              <tr>
                <td class="p-2 flex items-center gap-x-2">{api.name}<p class="text-xs text-gray-400">(ID: {api.id})</p></td>
                <td class="p-2">**********</td>
              </tr>
            {/each}
          </tbody>
        </table>
      {/if}
    </div>
  </div>

  <!-- Create API Button -->
  <Dialog.Root bind:open={dialogOpen}>
    <Dialog.Trigger>
      <Button class="ml-10 px-8 py-2 bg-blue-800 transition hover:bg-blue-700 hover:transition text-white rounded-lg">+ Create API</Button>
    </Dialog.Trigger>
    <Dialog.Content>
      <Dialog.Header>
        <Dialog.Title>Create API Key</Dialog.Title>
        {#if apiCreationSuccess}
          <Dialog.Description class="text-green-600">API key has been created successfully.</Dialog.Description>
          <div class="mt-4">
            <Label for="new-api-key">Your new API key:</Label>
            <div class="flex mt-2">
              <Input id="new-api-key" value={newApiKey} readonly class="flex-grow" />
              <Button 
                variant="outline"
                class="ml-2 px-4 py-2 bg-blue-800 text-white rounded-lg hover:bg-blue-700 hover:text-white focus:outline-none"
                on:click={copyToClipboard}
              >
                {copiedText}
              </Button>
            </div>
          </div>
        {:else}
        <Dialog.Description>
          Create a name for your API key.
        </Dialog.Description>
        <div class="grid gap-4 py-4">
          <div class="grid grid-cols-5 items-center gap-4">
            <Label for="name" class="text-right">Name</Label>
            <Input id="name" bind:value={newName} class="col-span-4" />
          </div>
        </div>
        <Dialog.Footer>
          <Button class="px-4 py-2 bg-blue-800 text-white rounded-lg hover:bg-blue-700 focus:outline-none" on:click={createAPI} disabled={creatingAPI}>
            {creatingAPI ? "Creating" : "Create API"}
          </Button>
        </Dialog.Footer>
        {/if}
      </Dialog.Header>
    </Dialog.Content>
  </Dialog.Root>

  <!-- Delete API Button -->
  <Dialog.Root>
    <Dialog.Trigger>
      <Button class="ml-10 px-8 py-2 bg-red-800 transition hover:bg-red-700 hover:transition text-white rounded-lg">- Delete API</Button></Dialog.Trigger>
    <Dialog.Content>
      <Dialog.Header>
        <Dialog.Title>Delete API</Dialog.Title>
        <Dialog.Description>
          Select which key you would like to remove. Please note that this action is irreversible.
        </Dialog.Description>
        <div class="space-y-4 py-4">
          {#if $query.isSuccess}
          <div class="grid grid-cols-5 items-center gap-4">
            <Label for="remove-key" class="text-right">API</Label>
            <div class="col-span-4">
              <Popover.Root bind:open let:ids>
                <Popover.Trigger asChild let:builder>
                  <Button
                    builders={[builder]}
                    variant="outline"
                    role="combobox"
                    aria-expanded={open}
                    class="w-full justify-between"
                  >
                    {selectedRemoveValue}
                    <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
                  </Button>
                </Popover.Trigger>
                <Popover.Content class="w-[72%] p-0">
                  <Command.Root>
                    <Command.Input placeholder="Search key..." />
                    <Command.Empty>No key found.</Command.Empty>
                    <Command.Group>
                      {#each $query.data as api}
                        <Command.Item
                          value={`${api.name} (ID: ${api.id})`}
                          onSelect={() => {
                            selectedAPItoDelete = { id: api.id, name: api.name };
                            closeAndFocusTrigger(ids.trigger);
                            open = false;
                          }}
                        >
                          <Check
                            class={cn(
                              "mr-2 h-4 w-4",
                              selectedAPItoDelete?.id !== api.id && "text-transparent"
                            )}
                          />
                          {api.name} (ID: {api.id})
                        </Command.Item>
                      {/each}
                    </Command.Group>
                  </Command.Root>
                </Popover.Content>
              </Popover.Root>
            </div>
          </div>
          {/if}
        </div>
        <Dialog.Footer>
          <DialogPrimitive.Close>
            <Button class="px-4 py-2 bg-red-800 text-white rounded-lg hover:bg-red-700 focus:outline-none" on:click={deleteAPI}>Remove Key</Button>
          </DialogPrimitive.Close>
        </Dialog.Footer>
      </Dialog.Header>
    </Dialog.Content>
  </Dialog.Root>
</div>