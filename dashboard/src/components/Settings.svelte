<script lang="ts">
  import { DateTime } from 'luxon';
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";

  let enableNotifications = true;
  let darkMode = false;

  function save() {
    const current_date = DateTime.now().toISO();
    toast.success(`Settings has been saved.`, {
      description: `${current_date}`,
    })
  }
</script>

<div class="flex flex-col flex-1">
  <Toaster />
  <h1 class="p-8 pl-20 text-3xl font-bold bg-white border-b-2">Settings</h1>
  <div class="m-10 border rounded-lg bg-white shadow flex-1 overflow-auto">
    <h2 class="p-10 pb-4 leading-none text-2xl font-semibold border-b-2">Overview</h2>
    <div class="p-20 px-64">
      <!-- General Settings Section -->
      <div>
        <h3 class="text-xl font-semibold mb-4">General Settings</h3>
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div class="text-gray-700">Enable Notifications</div>
            <label class="cursor-pointer relative inline-block w-14 h-8">
              <input type="checkbox" bind:checked={enableNotifications} class="opacity-0 w-0 h-0" />
              <span
                class="absolute top-0 left-0 right-0 bottom-0 rounded-full transition duration-200 ease-in-out"
                class:bg-gray-400={!enableNotifications} class:bg-blue-800={enableNotifications}>
              </span>
              <span
                class="absolute left-1 top-1 w-6 h-6 bg-white rounded-full transition transform duration-200 ease-in-out"
                class:translate-x-6={enableNotifications}>
              </span>
          </div>
          <div class="flex items-center justify-between">
            <div class="text-gray-700">Dark Mode</div>
            <label class="cursor-pointer relative inline-block w-14 h-8">
              <input type="checkbox" bind:checked={darkMode} class="opacity-0 w-0 h-0" />
              <span
                class="absolute top-0 left-0 right-0 bottom-0 rounded-full transition duration-200 ease-in-out"
                class:bg-gray-400={!darkMode} class:bg-blue-800={darkMode}>
              </span>
              <span
                class="absolute left-1 top-1 w-6 h-6 bg-white rounded-full transition transform duration-200 ease-in-out"
                class:translate-x-6={darkMode}>
              </span>
            </label>
          </div>
        </div>
      </div>
      <!-- Save Changes Button -->
      <div class="pt-6">
        <button on:click={save} class="px-4 py-2 bg-blue-800 text-white rounded-lg hover:bg-blue-700 focus:outline-none">Save Changes</button>
      </div>
    </div>
  </div>
</div>
