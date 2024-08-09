<script lang="ts">
  import { DateTime } from 'luxon';
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";
  import { Button } from "$lib/components/ui/button";
  import { Switch } from "$lib/components/ui/switch";
  import { Label } from "$lib/components/ui/label";

  let enableNotifications = true;
  let darkMode = false;

  function save() {
    const formatted_date = DateTime.now().toFormat('yyyy-MM-dd HH:mm:ss');
    toast.success(`Settings has been saved.`, {
      description: `${formatted_date}`,
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
            <Label for="notifications" class="text-gray-700">Enable Notifications</Label>
            <Switch id="notifications" bind:checked={enableNotifications} />
          </div>
          <div class="flex items-center justify-between">
            <Label for="darkMode" class="text-gray-700">Dark Mode</Label>
            <Switch id="darkMode" bind:checked={darkMode} />
          </div>
        </div>
      </div>
      <!-- Save Changes Button -->
      <div class="pt-6">
        <Button on:click={save} class="px-4 py-2 bg-blue-800 text-white rounded-lg hover:bg-blue-700 focus:outline-none">Save Changes</Button>
      </div>
    </div>
  </div>
</div>
