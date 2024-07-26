<script lang="ts">
  import { createQuery, useQueryClient } from '@tanstack/svelte-query';
  import Select from 'svelte-select';
  import { DateTime } from 'luxon';
  import * as Dialog from "$lib/components/ui/dialog";
  import { Input } from "$lib/components/ui/input/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import { Dialog as DialogPrimitive } from "bits-ui";
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";

  const items = ['OpenAI', 'Hugging Face', 'Google', 'Azure', 'Cohere', 'Mistral'];
  const token = localStorage.getItem("authToken");
  const userid = localStorage.getItem("userid");
  const queryClient = useQueryClient();

  type Repo = {
    name: string;
    last_used: string | null;
    user_id: number;
    id: number;
    key: string;
  };

  interface SecretOption {
    id: number;
    name: string;
  }

  let selectedSecret: SecretOption | null = null;
  let newName = { label: '', value: '' };
  let newKey = '';

  const addNewKey = async () => {
    const current_date = DateTime.now();
    const turso_date = current_date.toISO();
    const formatted_date = current_date.toFormat('yyyy-MM-dd HH:mm:ss');

    if (!newName.label || !newKey) {
      throw new Error('Please enter a provider and key');
    }
    const response = await fetch('http://127.0.0.1:8000/secrets/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        name: newName.label,
        key: newKey,
        last_used: turso_date,
      }),
    });
    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.statusText}`);
    }
    const undoSecret = await response.json();
    queryClient.invalidateQueries({ queryKey: ['repoData'] });
    toast.success(`${newName.label} has been added.`, {
      description: `${formatted_date}`,
      action: {
        label: "Undo",
        onClick: () => {
          selectedSecret = { id: undoSecret.id, name: undoSecret.name };
          removeKey()
        }
      }
    })
    newName = { label: '', value: '' };
    newKey = '';
  }

  const removeKey = async () => {
    const formatted_date = DateTime.now().toFormat('yyyy-MM-dd HH:mm:ss');

    if (!selectedSecret) {
      throw new Error('No secret selected for removal');
    }
    const response = await fetch(`http://127.0.0.1:8000/secrets/delete?secret_id=${selectedSecret.id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.statusText}`);
    }
    queryClient.invalidateQueries({ queryKey: ['repoData'] });
    toast.success(`${selectedSecret.name} has been removed.`, {
      description: `${formatted_date}`,
    });
    selectedSecret = null;
  }

  const fetchRepos = async (): Promise<Repo[]> => {
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
    return response.json();
  };

  const query = createQuery<Repo[]>({
    queryKey: ['repoData'],
    queryFn: fetchRepos,
  });
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
            {#each $query.data as repo}
              <tr>
                <td class="p-2">{repo.name}</td>
                <td class="p-2">**********</td>
                <td class="p-2">{DateTime.fromISO(repo.last_used ?? '').toRelative()}</td>
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
            <Select {items} bind:value={newName} class="col-span-4"/>
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
            <div>
              <div class="block text-gray-700">Select Secret to Remove</div>
              <select bind:value={selectedSecret} class="form-select mt-1 block w-full border rounded p-2 bg-white">
                <option value="" disabled selected>Select a key</option>
                {#each $query.data as repo}
                  <option value={{ id: repo.id, name: repo.name }}>
                    {repo.name}
                  </option>
                {/each}
              </select>
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