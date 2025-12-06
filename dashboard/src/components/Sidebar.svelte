<script lang="ts">
  import { navigate, Link, useLocation } from 'svelte-routing';
  import { auth } from '../stores/auth';
  import { Button } from "$lib/components/ui/button/index.js";
  import { MessageSquare, Bot, FileSliders, KeyRound, BarChart3, Wallet, UserRound, Settings, LogOut, Sun, Moon } from 'lucide-svelte';
  import Logo from './Logo.svelte';
  import { cn } from "$lib/utils";
  import { toggleMode } from "mode-watcher";

  const location = useLocation();
  $: currentPath = $location.pathname;

  const topMenuItems = [
    { path: '/chat', label: 'Chat', icon: MessageSquare },
    { path: '/myapi', label: 'MyAPI', icon: Bot },
    { path: '/configuration', label: 'Configuration', icon: FileSliders },
    { path: '/secrets', label: 'Secrets', icon: KeyRound },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 },
    { path: '/billing', label: 'Billing', icon: Wallet },
  ];

  const bottomMenuItems = [
    { path: '/account', label: 'Account', icon: UserRound },
    { path: '/settings', label: 'Settings', icon: Settings },
  ];

  function logout() {
    auth.logout();
    navigate('/login', { replace: true });
  }
</script>

<div class="w-64 bg-white dark:bg-slate-900 p-4 flex flex-col items-start border-r-2 dark:border-black">
  <div class="w-full flex justify-center mb-6">
    <Logo className="w-28 h-28"/>
  </div>
  <div class="font-semibold p-4 text-gray-400 dark:text-slate-400">MENU</div>
  <div class="flex flex-col justify-between space-y-2 w-full h-full">
    <div>
      {#each topMenuItems as { path, label, icon }}
        <Link to={path} class="w-full">
          <Button
            class={cn(
              "menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition bg-white dark:bg-slate-900",
              currentPath === path 
                ? 'bg-blue-100 dark:bg-blue-900 hover:bg-blue-200 hover:dark:bg-blue-800 text-blue-800 dark:text-blue-100' 
                : 'text-gray-500 dark:text-slate-200 hover:bg-gray-200 hover:dark:bg-slate-800 hover:text-gray-700 hover:dark:text-white'
            )}
            type="button"
          >
            <svelte:component this={icon} />
            <span class="font-semibold">{label}</span>
          </Button>
        </Link>
      {/each}
    </div>
    <div class="pb-8 pt-8 border-t-2 dark:border-black">
      {#each bottomMenuItems as { path, label, icon }}
        <Link to={path} class="w-full">
          <Button
            class={cn(
              "menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition bg-white dark:bg-slate-900",
              currentPath === path 
                ? 'bg-blue-100 dark:bg-blue-900 hover:bg-blue-200 hover:dark:bg-blue-800 text-blue-800 dark:text-blue-100' 
                : 'text-gray-500 dark:text-slate-200 hover:bg-gray-200 hover:dark:bg-slate-800 hover:text-gray-700 hover:dark:text-white'
            )}
            type="button"
          >
            <svelte:component this={icon} />
            <span class="font-semibold">{label}</span>
          </Button>
        </Link>
      {/each}
      <Button
        class="menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition bg-white dark:bg-slate-900 text-gray-500 dark:text-slate-200 hover:bg-gray-200 hover:dark:bg-slate-800 hover:text-gray-700 hover:dark:text-white"
        type="button"
        on:click={toggleMode}
      >
        <div class="relative w-[1.2rem] h-[1.2rem]">
          <Sun class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon class="absolute top-0 left-0 h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
        </div>
        <span class="font-semibold">Theme</span>
      </Button>

      <Button
        class="menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition bg-white dark:bg-slate-900 text-gray-500 dark:text-slate-200 hover:bg-gray-200 hover:dark:bg-slate-800 hover:text-gray-700 hover:dark:text-white"
        type="button"
        on:click={logout}
      >
        <LogOut />
        <span class="font-semibold">Logout</span>
      </Button>
    </div>
  </div>
</div>
