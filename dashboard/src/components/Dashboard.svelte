<script lang="ts">
  import { onMount } from 'svelte';

  type DataItem = {
    name: string;
    key: string;
    lastUsed: string;
  };

  let data: DataItem[] = [];

  onMount(async () => {
    const token = localStorage.getItem('authToken');
    if (!token) {
      alert('Not authenticated');
      window.location.href = '/';
      return;
    }

    // Dummy data for now
    data = [
      { name: 'Staging - User Analytics', key: 'babalane--...--1106', lastUsed: '10 days ago' },
      { name: 'Staging - User Analytics', key: 'babalane--...--1106', lastUsed: '10 days ago' }
    ];
  });
</script>

<div class="p-5">
  <h1 class="text-2xl font-bold">Dashboard</h1>
  <div class="mt-5">
    <table class="w-full border-collapse">
      <thead>
        <tr>
          <th class="border-b bg-gray-200 p-2 text-left">Name</th>
          <th class="border-b bg-gray-200 p-2 text-left">Key</th>
          <th class="border-b bg-gray-200 p-2 text-left">Last Used</th>
        </tr>
      </thead>
      <tbody>
        {#each data as item}
          <tr>
            <td class="border-b p-2">{item.name}</td>
            <td class="border-b p-2">{item.key}</td>
            <td class="border-b p-2">{item.lastUsed}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>
