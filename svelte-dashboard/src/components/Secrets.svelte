<script>
  let data = [
    { name: 'Staging - User Analytics', key: 'babalane--...--1106', lastUsed: '10 days ago' },
    { name: 'Staging - User Analytics', key: 'babalane--...--1106', lastUsed: '10 days ago' },
    { name: 'Staging - User Analytics', key: 'babalane--...--1106', lastUsed: '10 days ago' },
    { name: 'Staging - User Analytics', key: 'babalane--...--1106', lastUsed: '10 days ago' },
  ];

  let addKeyPopup = false;
  let newName = '';
  let newKey = '';

  function addNewKey() {
    data = [...data, { name: newName, key: newKey, lastUsed: 'Just now' }];
    newName = '';
    newKey = '';
    addKeyPopup = false;
  }
</script>

<div>
  <h1 class="p-8 pl-20 text-3xl font-bold bg-white border-b-2">Secrets</h1>
  <div class="m-10 border rounded-lg bg-white shadow">
    <h2 class="p-10 pb-4 leading-none text-2xl font-semibold border-b-2">Overview</h2>
    <div class="p-10">
      <table class="w-full">
        <thead>
          <tr>
            <th class="text-left p-2">Name</th>
            <th class="text-left p-2">Key</th>
            <th class="text-left p-2">Last Used</th>
          </tr>
        </thead>
        <tbody>
          {#each data as item}
            <tr>
              <td class="p-2">{item.name}</td>
              <td class="p-2">{item.key}</td>
              <td class="p-2">{item.lastUsed}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
  <button class="ml-10 px-8 py-2 bg-blue-800 transition hover:bg-blue-700 hover:transition text-white rounded-lg" on:click={() => addKeyPopup = true}>+ Add a new key</button>

  {#if addKeyPopup}
    <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
      <div class="bg-white rounded-lg shadow-lg p-8 w-96 relative">
        <button class="absolute pb-1 top-4 right-4 text-gray-500 hover:text-gray-700 text-4xl rounded-full h-12 w-12 flex items-center justify-center hover:bg-gray-200 transition duration-200 ease-in-out" on:click={() => addKeyPopup = false}>
          &times;
        </button>
        <h2 class="text-2xl font-semibold mb-4">Add New Key</h2>
        <div class="space-y-4">
          <div>
            <div class="block text-gray-700">Name</div>
            <input type="text" bind:value={newName} class="form-input mt-1 block w-full border rounded p-2" />
          </div>
          <div>
            <div class="block text-gray-700">Key</div>
            <input type="text" bind:value={newKey} class="form-input mt-1 block w-full border rounded p-2" />
          </div>
          <div class="pt-6">
            <button class="px-4 py-2 bg-blue-800 text-white rounded-lg hover:bg-blue-700 focus:outline-none" on:click={addNewKey}>Add Key</button>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>
