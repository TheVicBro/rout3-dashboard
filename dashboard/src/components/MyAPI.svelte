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
  import { z } from 'zod';

  const token = localStorage.getItem("authToken");
  const userid = localStorage.getItem("userid");
  const queryClient = useQueryClient();

  const APISchema = z.object({
    name: z.string(),
    key: z.string(),
    user_id: z.number(),
    id: z.number(),
  });

  const APIOptionSchema = z.object({
    id: z.number(),
    name: z.string(),
  });

  const NewSecretSchema = z.object({
    name: z.string().min(1, "Provider name is required"),
  });

  type Secret = z.infer<typeof APISchema>;
  type SelectedAPIOption = z.infer<typeof APIOptionSchema>;
  type NewSecret = z.infer<typeof NewSecretSchema>;

  let selectedAPItoDelete: SelectedAPIOption | null = null;

  const createAPI = async () => {
    const current_date = DateTime.now();
    const turso_date = current_date.toISO();
    const formatted_date = current_date.toFormat('yyyy-MM-dd HH:mm:ss');

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/create_key?name=${newName}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
      }
      queryClient.invalidateQueries({ queryKey: ['secretData'] });
      toast.success(`${newName} has been added.`, {
        description: `${formatted_date}`,
      })
      newName = '';
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

  const deleteAPI = async () => {
    const formatted_date = DateTime.now().toFormat('yyyy-MM-dd HH:mm:ss');

    try {
      if (!selectedAPItoDelete) {
        throw new Error('No secret selected for removal');
      }
      const validatedSecret = APIOptionSchema.parse(selectedAPItoDelete);

      const response = await fetch(`http://127.0.0.1:8000/api/remove_key?id=${validatedSecret.id}`, {
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

  const fetchSecrets = async (): Promise<Secret[]> => {
    const response = await fetch(`http://127.0.0.1:8000/api/get_key_by_user_id?user_id=${userid}`, {
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
    return z.array(APISchema).parse(data);
  };

  const query = createQuery<Secret[]>({
    queryKey: ['secretData'],
    queryFn: fetchSecrets,
  });

  const items = ['OpenAI', 'Hugging Face', 'Google', 'Azure', 'Cohere', 'Mistral'];

  let newName = '';
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
              <th class="text-left p-2">Name</th>
              <th class="text-left p-2">Key</th>
              <th class="text-left p-2">ID</th>
            </tr>
          </thead>
          <tbody>
            {#each $query.data as api}
              <tr>
                <td class="p-2">{api.name}</td>
                <td class="p-2">{api.key}</td>
                <td class="p-2">{api.id}</td>
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
          Select which key you would like to remove. Please note that this action is irreversible.
        </Dialog.Description>
        <div class="space-y-4 py-4">
          {#if $query.isSuccess}
            <div>
              <div class="block text-gray-700">Select API to Remove</div>
              <select bind:value={selectedAPItoDelete} class="form-select mt-1 block w-full border rounded p-2 bg-white">
                <option value="" disabled selected>Select a key</option>
                {#each $query.data as api}
                  <option value={{ id: api.id, name: api.name }}>
                    {api.name}
                  </option>
                {/each}
              </select>
            </div>
          {/if}
        </div>
        <Dialog.Footer>
          <DialogPrimitive.Close>
            <button class="px-4 py-2 bg-red-800 text-white rounded-lg hover:bg-red-700 focus:outline-none" on:click={deleteAPI}>Remove Key</button>
          </DialogPrimitive.Close>
        </Dialog.Footer>
      </Dialog.Header>
    </Dialog.Content>
  </Dialog.Root>
</div>