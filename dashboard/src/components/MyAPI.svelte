<script lang="ts">
  import { createQuery, useQueryClient } from '@tanstack/svelte-query';
  import * as Dialog from "$lib/components/ui/dialog";
  import { Input } from "$lib/components/ui/input/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import { Dialog as DialogPrimitive } from "bits-ui";

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

  const createAPI = async () => {
    const response = await fetch('http://127.0.0.1:8000/secrets/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        name: newName,
        key: newKey,
      }),
    });
    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.statusText}`);
    }
    queryClient.invalidateQueries({ queryKey: ['repoData'] });
    addAPIPopup = false;
  }

  const deleteAPI = async () => {
    if (selectedSecretId === null) {
      throw new Error('No secret selected for removal');
    }
    const response = await fetch(`http://127.0.0.1:8000/secrets/delete?secret_id=${selectedSecretId}`, {
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
    deleteAPIPopup = false;
  }

  const fetchRepos = async (): Promise<Repo[]> => {
    const response = await fetch(`http://127.0.0.1:8000/secrets/list?user_id=${userid}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Basic ${token}`,
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

  let addAPIPopup = false;
  let newName = '';
  let newKey = '';

  let deleteAPIPopup = false;
  let selectedSecretId: number | null = null;
</script>

<div>
  <h1 class="p-8 pl-20 text-3xl font-bold bg-white border-b-2">MyAPI</h1>
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
          <div class="mb-4 text-red-600">Create your first API key by clicking "Create API"</div>
        {/if}
        <table class="w-full">
          <thead>
            <tr>
              <th class="text-left p-2">Name</th>
              <th class="text-left p-2">Key</th>
              <th class="text-left p-2">Last Used</th>
            </tr>
          </thead>
          <tbody>
            {#each $query.data as repo}
              <tr>
                <td class="p-2">{repo.name}</td>
                <td class="p-2">**********</td>
                <td class="p-2">{repo.last_used}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      {/if}
    </div>
  </div>

  <!-- Create API Button -->
  <Dialog.Root>
    <Dialog.Trigger class="ml-10 px-8 py-2 bg-blue-800 transition hover:bg-blue-700 hover:transition text-white rounded-lg">+ Create API</Dialog.Trigger>
    <Dialog.Content>
      <Dialog.Header>
        <Dialog.Title>Create API Key</Dialog.Title>
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
          <DialogPrimitive.Close>
            <button class="px-4 py-2 bg-blue-800 text-white rounded-lg hover:bg-blue-700 focus:outline-none" on:click={createAPI}>Create API</button>
          </DialogPrimitive.Close>
        </Dialog.Footer>
      </Dialog.Header>
    </Dialog.Content>
  </Dialog.Root>

  <!-- Delete API Button -->
  <Dialog.Root>
    <Dialog.Trigger class="ml-10 px-8 py-2 bg-red-800 transition hover:bg-red-700 hover:transition text-white rounded-lg">- Delete API</Dialog.Trigger>
    <Dialog.Content>
      <Dialog.Header>
        <Dialog.Title>Delete API</Dialog.Title>
        <Dialog.Description>
          Select which API key you would like to delete. Please note that this action is irreversible.
        </Dialog.Description>
        {#if $query.isSuccess}
          <div>
            <select bind:value={selectedSecretId} class="form-select mt-1 block w-full border rounded p-2">
              <option value="" disabled selected>Select API key</option>
              {#each $query.data as repo}
                <option value={repo.id}>{repo.name}</option>
              {/each}
            </select>
          </div>
        {/if}
        <Dialog.Footer>
          <DialogPrimitive.Close>
            <button class="px-4 py-2 bg-red-800 text-white rounded-lg hover:bg-red-700 focus:outline-none" on:click={deleteAPI}>Delete API</button>
          </DialogPrimitive.Close>
        </Dialog.Footer>
      </Dialog.Header>
    </Dialog.Content>
  </Dialog.Root>
</div>
