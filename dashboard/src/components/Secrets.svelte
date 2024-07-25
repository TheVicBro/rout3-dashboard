<script lang="ts">
  import { createQuery, useQueryClient } from '@tanstack/svelte-query';
  import { DateTime } from 'luxon';
  import * as Dialog from "$lib/components/ui/dialog";
  import { Input } from "$lib/components/ui/input/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import { Dialog as DialogPrimitive } from "bits-ui";
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";
  import { z } from 'zod';
  import * as Command from "$lib/components/ui/command/index.js";
  import * as Popover from "$lib/components/ui/popover/index.js";
  import { Button } from "$lib/components/ui/button/index.js";
  import { cn } from "$lib/utils.js";
  import Check from "lucide-svelte/icons/check";
  import ChevronsUpDown from "lucide-svelte/icons/chevrons-up-down";
  import { availableModelProviders, closeAndFocusTrigger } from "../utils/utils"; 

  const token = localStorage.getItem("authToken");
  const userid = localStorage.getItem("userid");
  const queryClient = useQueryClient();

  const SecretSchema = z.object({
    name: z.string(),
    last_used: z.string(),
    user_id: z.number(),
    id: z.number(),
  });

  const SecretOptionSchema = z.object({
    id: z.number(),
    name: z.string(),
  });

  const NewSecretSchema = z.object({
    name: z.string().min(1, "Provider name is required"),
    key: z.string().min(1, "Key is required"),
    last_used: z.string(),
  });

  type Secret = z.infer<typeof SecretSchema>;
  type SecretOption = z.infer<typeof SecretOptionSchema>;
  type NewSecret = z.infer<typeof NewSecretSchema>;

  let selectedSecret: SecretOption | null = null;

  const addNewKey = async () => {
    const current_date = DateTime.now();
    const turso_date = current_date.toISO();
    const formatted_date = current_date.toFormat('yyyy-MM-dd HH:mm:ss');

    try {
      const newSecretData: NewSecret = NewSecretSchema.parse({
        name: newName,
        key: newKey,
        last_used: turso_date,
      });

      const response = await fetch('http://127.0.0.1:8000/secrets/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(newSecretData),
      });
      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
      }
      const undoSecret = SecretSchema.parse(await response.json());
      queryClient.invalidateQueries({ queryKey: ['secretData'] });
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
      newName = '';
      newKey = '';
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
  }

  const removeKey = async () => {
    const formatted_date = DateTime.now().toFormat('yyyy-MM-dd HH:mm:ss');

    try {
      if (!selectedSecret) {
        throw new Error('No secret selected for removal');
      }
      const validatedSecret = SecretOptionSchema.parse(selectedSecret);

      const response = await fetch(`http://127.0.0.1:8000/secrets/delete?secret_id=${validatedSecret.id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
      }
      queryClient.invalidateQueries({ queryKey: ['secretData'] });
      toast.success(`${selectedSecret.name} has been removed.`, {
        description: `${formatted_date}`,
      });
      selectedSecret = null;
    } catch (error) {
      toast.error("An error occurred", {
        description: error instanceof Error ? error.message : "Unknown error"
      });
    }
  }

  const fetchSecrets = async (): Promise<Secret[]> => {
    const response = await fetch(`http://127.0.0.1:8000/secrets/list?user_id=${userid}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      }
    });
    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.statusText}`);
    }
    const data = await response.json();
    return z.array(SecretSchema).parse(data);
  };

  const query = createQuery<Secret[]>({
    queryKey: ['secretData'],
    queryFn: fetchSecrets,
  });
 
  let open = false;
  $: selectedValue = availableModelProviders.find((f) => f === newName) ?? "Select a provider...";
  $: selectedRemoveValue = selectedSecret 
    ? `${selectedSecret.name} (ID: ${selectedSecret.id})` 
    : "Select a key to remove...";

  let newName = '';
  let newKey = '';
</script>

<div>
  <Toaster />
  <h1 class="p-8 pl-20 text-3xl font-bold bg-white border-b-2">Secrets</h1>
  <div class="m-10 border rounded-lg bg-white shadow">
    <h2 class="p-10 pb-4 leading-none text-2xl font-semibold border-b-2">Overview</h2>
    <div class="p-10">
      {#if $query.isPending}
        Loading...
      {/if}
      {#if $query.error}
        An error has occurred: {$query.error.message}
      {/if}
      {#if $query.isSuccess}
        {#if $query.data.length === 0}
          <div class="mb-4 text-red-600">No secrets found. Click "Add key" to add a new key.</div>
        {/if}
        <table class="w-full">
          <thead>
            <tr>
              <th class="text-left p-2">Provider</th>
              <th class="text-left p-2">Key</th>
              <th class="text-left p-2">Last Used</th>
            </tr>
          </thead>
          <tbody>
            {#each $query.data as secret}
              <tr>
                <td class="p-2 flex items-center gap-x-2">{secret.name} <p class="text-xs text-gray-400">(ID: {secret.id})</p></td>
                <td class="p-2">**********</td>
                <td class="p-2">{DateTime.fromISO(secret.last_used).toRelative()}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      {/if}
    </div>
  </div>

  <!-- Add Key Button -->
  <Dialog.Root>
    <Dialog.Trigger class="ml-10 px-8 py-2 bg-blue-800 transition hover:bg-blue-700 hover:transition text-white rounded-lg">+ Add a new key</Dialog.Trigger>
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
            <button class="px-4 py-2 bg-blue-800 text-white rounded-lg hover:bg-blue-700 focus:outline-none" on:click={addNewKey}>Add Key</button>
          </DialogPrimitive.Close>
        </Dialog.Footer>
      </Dialog.Header>
    </Dialog.Content>
  </Dialog.Root>

  <!-- Remove Key Button -->
  <Dialog.Root>
    <Dialog.Trigger class="ml-10 px-8 py-2 bg-red-800 transition hover:bg-red-700 hover:transition text-white rounded-lg">- Remove a key</Dialog.Trigger>
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
            <button class="px-4 py-2 bg-red-800 text-white rounded-lg hover:bg-red-700 focus:outline-none" on:click={removeKey}>Remove Key</button>
          </DialogPrimitive.Close>
        </Dialog.Footer>
      </Dialog.Header>
    </Dialog.Content>
  </Dialog.Root>
</div>