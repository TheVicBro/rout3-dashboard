<script lang="ts">
  import Sidebar from './Sidebar.svelte';
</script>

<div class="flex h-screen bg-slate-100 dark:bg-slate-800">
  <Sidebar />
  <div class="flex-1 flex flex-col overflow-hidden">
    <slot />
  </div>
</div>