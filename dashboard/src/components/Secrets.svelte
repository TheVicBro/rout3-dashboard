<script lang="ts">
<<<<<<< HEAD
  import { createQuery, useQueryClient } from "@tanstack/svelte-query";
=======
  import { createQuery, useQueryClient } from '@tanstack/svelte-query';
  import Select from 'svelte-select';
>>>>>>> 34c65d5 (Added drop down list for secrets, begun work on MyAPI page)

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

  const addNewKey = async () => {
    const response = await fetch("http://127.0.0.1:8000/secrets/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        name: newName.label,
        key: newKey,
      }),
    });
    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.statusText}`);
    }
<<<<<<< HEAD
    queryClient.invalidateQueries({ queryKey: ["repoData"] });
=======
    queryClient.invalidateQueries({ queryKey: ['repoData'] });
    newName = { label: '', value: '' };
    newKey = '';
>>>>>>> 34c65d5 (Added drop down list for secrets, begun work on MyAPI page)
    addKeyPopup = false;
  };

  const removeKey = async () => {
    if (selectedSecretId === null) {
      throw new Error("No secret selected for removal");
    }
    const response = await fetch(
      `http://127.0.0.1:8000/secrets/delete?secret_id=${selectedSecretId}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      },
    );
    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.statusText}`);
    }
    queryClient.invalidateQueries({ queryKey: ["repoData"] });

    removeKeyPopup = false;
  };

  const fetchRepos = async (): Promise<Repo[]> => {
    const response = await fetch(
      `http://127.0.0.1:8000/secrets/list?user_id=${userid}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Basic ${token}`,
        },
      },
    );
    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.statusText}`);
    }
    return response.json();
  };

  const query = createQuery<Repo[]>({
    queryKey: ["repoData"],
    queryFn: fetchRepos,
  });

  const items = ['OpenAI', 'Hugging Face', 'Google', 'Azure', 'Cohere', 'Mistral'];
  $: filteredItems = items.filter(item => !($query.data ?? []).some(repo => repo.name === item));

  let addKeyPopup = false;
<<<<<<< HEAD
  let newName = "";
  let newKey = "";
=======
  let newName = { label: '', value: '' };
  let newKey = '';
>>>>>>> 34c65d5 (Added drop down list for secrets, begun work on MyAPI page)

  let removeKeyPopup = false;
  let selectedSecretId: number | null = null;
</script>

<div>
  <h1 class="p-8 pl-20 text-3xl font-bold bg-white border-b-2">Secrets</h1>
  <div class="m-10 border rounded-lg bg-white shadow">
    <h2 class="p-10 pb-4 leading-none text-2xl font-semibold border-b-2">
      Overview
    </h2>
    <div class="p-10">
      {#if $query.isPending}
        Loading...
      {/if}
      {#if $query.error}
        An error has occurred: {$query.error.message}
      {/if}
      {#if $query.isSuccess}
        {#if $query.data.length === 0}
          <div class="mb-4 text-red-600">
            No secrets found. Click "Add key" to add a new key.
          </div>
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
                <td class="p-2">{repo.last_used}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      {/if}
    </div>
  </div>
<<<<<<< HEAD
  <button
    class="ml-10 px-8 py-2 bg-blue-800 transition hover:bg-blue-700 hover:transition text-white rounded-lg"
    on:click={() => (addKeyPopup = true)}>+ Add a new key</button
  >
  <button
    class="ml-10 px-8 py-2 bg-blue-800 transition hover:bg-blue-700 hover:transition text-white rounded-lg"
    on:click={() => (removeKeyPopup = true)}>+ Remove a key</button
  >
=======
  <button class="ml-10 px-8 py-2 bg-blue-800 transition hover:bg-blue-700 hover:transition text-white rounded-lg" on:click={() => addKeyPopup = true}>+ Add a new key</button>
  <button class="ml-10 px-8 py-2 bg-red-800 transition hover:bg-red-700 hover:transition text-white rounded-lg" on:click={() => removeKeyPopup = true}>- Remove a key</button>
>>>>>>> 34c65d5 (Added drop down list for secrets, begun work on MyAPI page)

  {#if addKeyPopup}
    <div
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
    >
      <div class="bg-white rounded-lg shadow-lg p-8 w-96 relative">
        <button
          class="absolute pb-1 top-4 right-4 text-gray-500 hover:text-gray-700 text-4xl rounded-full h-12 w-12 flex items-center justify-center hover:bg-gray-200 transition duration-200 ease-in-out"
          on:click={() => (addKeyPopup = false)}
        >
          &times;
        </button>
        <h2 class="text-2xl font-semibold mb-4">Add New Key</h2>
        <div class="space-y-4">
          <div>
<<<<<<< HEAD
            <div class="block text-gray-700">Name</div>
            <input
              type="text"
              bind:value={newName}
              class="form-input mt-1 block w-full border rounded p-2"
            />
=======
            <div class="block text-gray-700">Provider</div>
            <Select items={filteredItems} bind:value={newName} />
>>>>>>> 34c65d5 (Added drop down list for secrets, begun work on MyAPI page)
          </div>
          <div>
            <div class="block text-gray-700">Key</div>
            <input
              type="text"
              bind:value={newKey}
              class="form-input mt-1 block w-full border rounded p-2"
            />
          </div>
          <div class="pt-6">
            <button
              class="px-4 py-2 bg-blue-800 text-white rounded-lg hover:bg-blue-700 focus:outline-none"
              on:click={addNewKey}>Add Key</button
            >
          </div>
        </div>
      </div>
    </div>
  {/if}

  {#if removeKeyPopup}
    <div
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
    >
      <div class="bg-white rounded-lg shadow-lg p-8 w-96 relative">
        <button
          class="absolute pb-1 top-4 right-4 text-gray-500 hover:text-gray-700 text-4xl rounded-full h-12 w-12 flex items-center justify-center hover:bg-gray-200 transition duration-200 ease-in-out"
          on:click={() => (removeKeyPopup = false)}
        >
          &times;
        </button>
        <h2 class="text-2xl font-semibold mb-4">Remove Key</h2>
        <div class="space-y-4">
          {#if $query.isSuccess}
            <div>
              <div class="block text-gray-700">Select Secret to Remove</div>
              <select
                bind:value={selectedSecretId}
                class="form-select mt-1 block w-full border rounded p-2"
              >
                <option value="" disabled selected>Select a key</option>
                {#each $query.data as repo}
                  <option value={repo.id}>{repo.name}</option>
                {/each}
              </select>
            </div>
          {/if}
          <div class="pt-6">
<<<<<<< HEAD
            <button
              class="px-4 py-2 bg-blue-800 text-white rounded-lg hover:bg-blue-700 focus:outline-none"
              on:click={removeKey}>Remove Key</button
            >
=======
            <button class="px-4 py-2 bg-red-800 text-white rounded-lg hover:bg-red-700 focus:outline-none" on:click={removeKey}>Remove Key</button>
>>>>>>> 34c65d5 (Added drop down list for secrets, begun work on MyAPI page)
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>
