<script lang="ts">
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';

  const modelProviders = ["OpenAI", "Hugging Face", "Google AI", "Microsoft Azure"];
  const selectedModel = writable(modelProviders[0]);
  const temperature = writable(0.7);
  const maxTokens = writable(100);
  const guardRails = writable<string[]>([""]);

  function setupModel() {
    // Mock function to simulate model setup
    alert(`Model from ${$selectedModel} set up with temperature ${$temperature} and max tokens ${$maxTokens}.`);
    document.getElementById('model-iframe').style.display = 'block';
  }

  function addGuardRail() {
    guardRails.update(gr => [...gr, ""]);
  }

  function updateGuardRail(index: number, value: string) {
    guardRails.update(gr => {
      gr[index] = value;
      return gr;
    });
  }

  function removeGuardRail(index: number) {
    guardRails.update(gr => {
      gr.splice(index, 1);
      return gr;
    });
  }
</script>

<div class="flex flex-col flex-1">
  <h1 class="p-8 pl-20 text-3xl font-bold bg-white border-b-2">MyAI</h1>
  <div class="m-10 border rounded-lg bg-white shadow flex-1 overflow-auto">
    <h2 class="p-10 pb-4 leading-none text-2xl font-semibold border-b-2">Overview</h2>
    <div class="p-20 px-64">
      <h3 class="text-xl font-semibold mb-4">Select a Model Provider</h3>
      <select bind:value={$selectedModel} class="border p-2 rounded mb-4">
        {#each modelProviders as provider}
          <option value={provider}>{provider}</option>
        {/each}
      </select>

      <h3 class="text-xl font-semibold mb-4">Model Settings</h3>
      <div class="mb-4">
        <label for="temperature" class="block font-semibold mb-1">Temperature</label>
        <input id="temperature" type="range" min="0" max="1" step="0.01" bind:value={$temperature} class="w-full" />
        <span>{($temperature).toFixed(2)}</span>
      </div>
      <div class="mb-4">
        <label for="maxTokens" class="block font-semibold mb-1">Max Tokens</label>
        <input id="maxTokens" type="number" min="1" max="1000" bind:value={$maxTokens} class="w-full border p-2 rounded" />
      </div>

      <h3 class="text-xl font-semibold mb-4">Guard Rails</h3>
      {#each $guardRails as guardRail, index}
        <div class="mb-4 flex items-center">
          <input
            type="text"
            class="w-full border p-2 rounded mb-2"
            placeholder="Add guard rail"
            bind:value={$guardRails[index]}
            on:input={(e) => updateGuardRail(index, e.target.value)}
          />
          {#if index > 0}
            <button on:click={() => removeGuardRail(index)} class="ml-2 text-red-500 hover:text-red-700">Remove</button>
          {/if}
        </div>
      {/each}
      <button on:click={addGuardRail} class="px-4 py-2 text-white rounded-lg bg-red-800 hover:bg-red-700 transition mb-4">Add Guard Rail</button>

      <button on:click={setupModel} class="px-4 py-2 text-white rounded-lg bg-blue-800 hover:bg-blue-700 transition">Set Up Model</button>

      <div id="model-iframe" style="display: none;" class="mt-8 border rounded overflow-hidden">
        <iframe src="https://example.com" class="w-full h-96"></iframe>
      </div>
    </div>
  </div>
</div>
