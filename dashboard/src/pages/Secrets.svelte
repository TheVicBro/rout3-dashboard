<script lang="ts">
  import { createQuery, useQueryClient } from '@tanstack/svelte-query';
  import { DateTime } from 'luxon';
  import { Input } from "$lib/components/ui/input/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import { Dialog as DialogPrimitive } from "bits-ui";
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";
  import { z } from 'zod';
  import { Button } from "$lib/components/ui/button/index.js";
  import { CirclePlus, Check, ChevronsUpDown } from "lucide-svelte";
  import { cn, availableModelProviders, closeAndFocusTrigger } from "$lib/utils"; 
  import * as Dialog from "$lib/components/ui/dialog";
  import * as Command from "$lib/components/ui/command/index.js";
  import * as Popover from "$lib/components/ui/popover/index.js";
  import Skeleton from "../components/Skeleton.svelte"
  import { api } from "$lib/api";

  const queryClient = useQueryClient();

  const SecretSchema = z.object({
    name: z.string(),
    last_used: z.string().nullable(),
    user_id: z.number(),
    id: z.number(),
  });

  const SecretOptionSchema = z.object({
    id: z.number(),
    name: z.string(),
  });

  const NewSecretSchema = z.object({
    name: z.string().min(1, "Provider name is required"),
    last_used: z.string().nullable(),
    key: z.string().min(1, "Key is required"),
  });

  type Secret = z.infer<typeof SecretSchema>;
  type SecretOption = z.infer<typeof SecretOptionSchema>;
  type NewSecret = z.infer<typeof NewSecretSchema>;

  let selectedSecret: SecretOption | null = null;
  let newName = '';
  let newKey = '';
  let open = false;

  const addNewKey = async () => {
    const current_date = DateTime.local();
    const turso_date = current_date.toISO();
    const formatted_date = current_date.toFormat('yyyy-MM-dd HH:mm:ss');

    try {
      const newSecretData: NewSecret = NewSecretSchema.parse({
        name: newName,
        last_used: turso_date,
        key: newKey,
      });

      const undoSecret = await api.post<Secret>('/secrets', newSecretData);
      
      await queryClient.invalidateQueries({ queryKey: ['secretData'] });
      toast.success(`${newName} has been added.`, {
        description: `${formatted_date}`,
        action: {
          label: "Undo",
          onClick: () => {
            selectedSecret = { id: undoSecret.id, name: undoSecret.name };
            removeKey()
          }
        }
      })
    } catch (error) {
      handleError(error);
    }
    newName = '';
    newKey = '';
  }

  const removeKey = async () => {
    const formatted_date = DateTime.now().toFormat('yyyy-MM-dd HH:mm:ss');

    try {
      if (!selectedSecret) {
        throw new Error('No secret selected for removal');
      }
      const validatedSecret = SecretOptionSchema.parse(selectedSecret);

      await api.delete(`/secrets/${validatedSecret.id}`);

      await queryClient.invalidateQueries({ queryKey: ['secretData'] });
      toast.success(`${selectedSecret.name} has been removed.`, {
        description: `${formatted_date}`,
      });
    } catch (error) {
      handleError(error);
    }
    selectedSecret = null;
  }

  const fetchSecrets = async (): Promise<Secret[]> => {
    const data = await api.get<unknown>('/secrets');
    return z.array(SecretSchema).parse(data);
  };

  const query = createQuery<Secret[]>({
    queryKey: ['secretData'],
    queryFn: fetchSecrets,
  });

  const handleError = (error: unknown) => {
    if (error instanceof z.ZodError) {
      toast.error("Validation error", {
        description: error.errors.map(e => e.message).join(", ")
      });
    } else {
      toast.error("An error occurred", {
        description: error instanceof Error ? error.message : "Unknown error"
      });
    }
  };
 
  $: selectedValue = availableModelProviders.find((f) => f === newName) ?? "Select a provider...";
  $: selectedRemoveValue = selectedSecret 
    ? `${selectedSecret.name} (ID: ${selectedSecret.id})` 
    : "Select a key to remove...";
</script>

<div>
  <Toaster />
  <h1 class="p-8 text-3xl font-bold bg-white dark:bg-slate-900 border-b dark:border-slate-800">Secrets</h1>
  <div class="m-10 space-y-6">
    <div class="bg-white dark:bg-slate-900 rounded-lg border dark:border-slate-800 shadow-sm overflow-hidden">
      {#if $query.isPending}
        <div class="p-10">
          <Skeleton />
        </div>
      {:else if $query.error}
        <div class="p-10">
          <p class="text-red-600">An error has occurred: {$query.error.message}</p>
        </div>
      {:else if $query.data.length === 0}
        <div class="flex flex-col items-center p-10">
          <CirclePlus class="w-12 h-12 mb-4 text-gray-400" />
          <p>No secrets found. Click "Add key" to add a new key.</p>
        </div>
      {:else}
        <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-slate-800 dark:text-gray-400">
            <tr>
              <th class="px-6 py-3">Provider</th>
              <th class="px-6 py-3">Key</th>
              <th class="px-6 py-3">Last Used</th>
            </tr>
          </thead>
          <tbody>
            {#each $query.data as secret}
              <tr class="bg-white border-b dark:bg-slate-900 dark:border-slate-800 hover:bg-gray-50 dark:hover:bg-slate-800/50">
                <td class="px-6 py-4 font-medium text-gray-900 dark:text-white whitespace-nowrap flex items-center gap-x-2">
                  {secret.name}
                  <span class="text-xs text-gray-400 font-normal">(ID: {secret.id})</span>
                </td>
                <td class="px-6 py-4 font-mono">**********</td>
                <td class="px-6 py-4">
                  {secret.last_used 
                    ? DateTime.fromISO(secret.last_used).setZone(DateTime.local().zoneName).toRelative()
                    : "Never Used"}
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      {/if}
    </div>

    <div class="flex gap-4">
      <!-- Add Key Button -->
      <Dialog.Root>
        <Dialog.Trigger>
          <Button class="px-8 py-2">+ Add a new key</Button>
        </Dialog.Trigger>
    <Dialog.Content>
      <Dialog.Header>
        <Dialog.Title>Add New Key</Dialog.Title>
        <Dialog.Description>
          Select a provider and enter a key to add a new key.
        </Dialog.Description>
        <div class="grid gap-4 py-4">
          <div class="grid grid-cols-5 items-center gap-4">
            <Label for="provider" class="text-right">Provider</Label>
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
                    {selectedValue}
                    <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
                  </Button>
                </Popover.Trigger>
                <Popover.Content class="w-[72%] p-0">
                  <Command.Root>
                    <Command.Input placeholder="Search provider..." />
                    <Command.Empty>No provider found.</Command.Empty>
                    <Command.Group>
                      {#each availableModelProviders as provider}
                        <Command.Item
                          value={provider}
                          onSelect={(currentValue) => {
                            newName = currentValue;
                            closeAndFocusTrigger(ids.trigger);
                            open = false;
                          }}
                        >
                          <Check
                            class={cn(
                              "mr-2 h-4 w-4",
                              newName !== provider && "text-transparent"
                            )}
                          />
                          {provider}
                        </Command.Item>
                      {/each}
                    </Command.Group>
                  </Command.Root>
                </Popover.Content>
              </Popover.Root>
            </div>
          </div>
          <div class="grid grid-cols-5 items-center gap-4">
            <Label for="key" class="text-right">Key</Label>
            <Input id="key" bind:value={newKey} class="col-span-4" />
          </div>
        </div>
        <Dialog.Footer>
          <DialogPrimitive.Close>
            <Button class="px-4 py-2" on:click={addNewKey}>Add Key</Button>
          </DialogPrimitive.Close>
        </Dialog.Footer>
      </Dialog.Header>
    </Dialog.Content>
  </Dialog.Root>

      <!-- Remove Key Button -->
      <Dialog.Root>
        <Dialog.Trigger>
          <Button variant="destructive" class="px-8 py-2">- Remove a key</Button>
        </Dialog.Trigger>
        <Dialog.Content>
      <Dialog.Header>
        <Dialog.Title>Remove Key</Dialog.Title>
        <Dialog.Description>
          Select which key you would like to remove. Please note that this action is irreversible.
        </Dialog.Description>
        <div class="space-y-4 py-4">
          {#if $query.isSuccess}
            <div class="grid grid-cols-5 items-center gap-4">
              <Label for="remove-key" class="text-right">Secret</Label>
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
                        {#each $query.data as secret}
                          <Command.Item
                            value={`${secret.name} (ID: ${secret.id})`}
                            onSelect={() => {
                              selectedSecret = { id: secret.id, name: secret.name };
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
            <Button variant="destructive" class="px-4 py-2" on:click={removeKey}>Remove Key</Button>
          </DialogPrimitive.Close>
        </Dialog.Footer>
      </Dialog.Header>
    </Dialog.Content>
  </Dialog.Root>
    </div>
  </div>
</div>