<script lang="ts">
  import { onMount } from 'svelte';
  import { DateTime } from 'luxon';
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";
  import { Button } from "$lib/components/ui/button";
  import { Switch } from "$lib/components/ui/switch";
  import { Label } from "$lib/components/ui/label";
  import { toggleMode } from "mode-watcher";

  let enableNotifications = true;
  let darkMode = false;

  onMount(() => {
    darkMode = document.documentElement.classList.contains('dark');
  });

  function save() {
    const formatted_date = DateTime.now().toFormat('yyyy-MM-dd HH:mm:ss');
    toast.success(`Settings has been saved.`, {
      description: `${formatted_date}`,
    })
  }
</script>

<div class="flex flex-col flex-1">
  <Toaster />
  <h1 class="p-8 text-3xl font-bold bg-white dark:bg-slate-900 border-b dark:border-slate-800">Settings</h1>
  <div class="m-10 bg-white dark:bg-slate-900 rounded-lg border dark:border-slate-800 shadow-sm flex-1 overflow-auto">
    <h2 class="p-8 text-xl font-semibold border-b dark:border-slate-800">Overview</h2>
    <div class="p-20 px-64">
      <div>
        <h3 class="text-xl font-semibold mb-4">General Settings</h3>
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <Label for="notifications" class="text-gray-700 dark:text-white">Enable Notifications</Label>
            <Switch id="notifications" bind:checked={enableNotifications} />
          </div>
          <div class="flex items-center justify-between">
            <Label for="darkMode" class="text-gray-700 dark:text-white">Dark Mode</Label>
            <Switch id="darkMode" on:click={toggleMode} bind:checked={darkMode} />
          </div>
        </div>
      </div>
      <div class="pt-6">
        <Button on:click={save} class="px-4 py-2">Save Changes</Button>
      </div>
    </div>
  </div>
</div>
