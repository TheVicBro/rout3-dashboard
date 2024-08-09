<script lang="ts">
  import { Link, useLocation } from 'svelte-routing';
  import { isAuthenticated } from '../stores/auth';
  import { Button } from "$lib/components/ui/button/index.js";
  import { Bot, FileSliders, KeyRound, BarChart3, Wallet, UserRound, Settings, LogOut } from 'lucide-svelte';
  import logo from '/llmproxyTransparent.png';

  const location = useLocation();
  $: currentPath = $location.pathname;

  const topMenuItems = [
    { path: '/myapi', label: 'MyAPI', icon: Bot },
    { path: '/configuration', label: 'Configuration', icon: FileSliders },
    { path: '/secrets', label: 'Secrets', icon: KeyRound },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 },
    { path: '/billing', label: 'Billing', icon: Wallet },
  ];

  const bottomMenuItems = [
    { path: '/account', label: 'Account', icon: UserRound },
    { path: '/settings', label: 'Settings', icon: Settings },
    { path: '/login', label: 'Logout', icon: LogOut, onClick: logout },
  ];

  function logout() {
    localStorage.clear();
    isAuthenticated.set(false);
  }
</script>

<div class="w-64 bg-white p-4 flex flex-col items-start border-r-2">
  <div class="w-full flex justify-center mb-6">
    <img src={logo} alt="Logo" class="w-28 h-28" />
  </div>
  <div class="font-semibold p-4 text-gray-400">MENU</div>
  <div class="flex flex-col justify-between space-y-2 w-full h-full">
    <div>
      {#each topMenuItems as { path, label, icon }}
        <Link to={path} class="w-full">
          <Button
            class={`menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition bg-white ${
              currentPath === path ? 'bg-blue-100 hover:bg-blue-200 text-blue-800' : 'text-gray-500 hover:bg-gray-200 hover:text-gray-700'
            }`}
            type="button"
          >
            <svelte:component this={icon} />
            <span class="font-semibold">{label}</span>
          </Button>
        </Link>
      {/each}
    </div>
    <div class="pb-8 pt-8 border-t-2">
      {#each bottomMenuItems as { path, label, icon, onClick }}
        <Link to={path} class="w-full">
          <Button
            class={`menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition bg-white ${
              currentPath === path ? 'bg-blue-100 hover:bg-blue-200 text-blue-800' : 'text-gray-500 hover:bg-gray-200 hover:text-gray-700'
            }`}
            type="button"
            on:click={onClick}
          >
            <svelte:component this={icon} />
            <span class="font-semibold">{label}</span>
          </Button>
        </Link>
      {/each}
    </div>
  </div>
</div>
