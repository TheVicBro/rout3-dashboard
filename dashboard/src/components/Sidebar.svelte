<script lang="ts">
  import { Link, useLocation } from 'svelte-routing';
  import logo from '/llmproxyTransparent.png';
  import { isAuthenticated } from '../stores/auth';
  
  // Get the current location
  const location = useLocation();

  // Reactive statement to track the current path
  $: currentPath = $location.pathname;

  function logout() {
    localStorage.removeItem('authToken');
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
      <Link to="/myai" class="w-full">
        <button
          class={`menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition ${
            currentPath === '/myai' ? 'bg-blue-100 text-blue-800' : 'text-gray-500 hover:bg-gray-200 hover:text-gray-700'
          }`}
          type="button"
        >
          <i class="icon-key"></i>
          <span class="font-semibold">MyAI</span>
        </button>
      </Link>
      <Link to="/secrets" class="w-full">
        <button
          class={`menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition ${
            currentPath === '/secrets' ? 'bg-blue-100 text-blue-800' : 'text-gray-500 hover:bg-gray-200 hover:text-gray-700'
          }`}
          type="button"
        >
          <i class="icon-key"></i>
          <span class="font-semibold">Secrets</span>
        </button>
      </Link>
      <Link to="/analytics" class="w-full">
        <button
          class={`menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition ${
            currentPath === '/analytics' ? 'bg-blue-100 text-blue-800' : 'text-gray-500 hover:bg-gray-200 hover:text-gray-700'
          }`}
          type="button"
        >
          <i class="icon-analytics"></i>
          <span class="font-semibold">Analytics</span>
        </button>
      </Link>
      <Link to="/billing" class="w-full">
        <button
          class={`menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition ${
            currentPath === '/billing' ? 'bg-blue-100 text-blue-800' : 'text-gray-500 hover:bg-gray-200 hover:text-gray-700'
          }`}
          type="button"
        >
          <i class="icon-billing"></i>
          <span class="font-semibold">Billing</span>
        </button>
      </Link>
    </div>
    <div class="pb-8 pt-8 border-t-2">
      <Link to="/account" class="w-full">
        <button
          class={`menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition ${
            currentPath === '/account' ? 'bg-blue-100 text-blue-800' : 'text-gray-500 hover:bg-gray-200 hover:text-gray-700'
          }`}
          type="button"
        >
          <i class="icon-account"></i>
          <span class="font-semibold">Account</span>
        </button>
      </Link>
      <Link to="/settings" class="w-full">
        <button
          class={`menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition ${
            currentPath === '/settings' ? 'bg-blue-100 text-blue-800' : 'text-gray-500 hover:bg-gray-200 hover:text-gray-700'
          }`}
          type="button"
        >
          <i class="icon-settings"></i>
          <span class="font-semibold">Settings</span>
        </button>
      </Link>
      <Link to="/login" class="w-full">
        <button
          class="menu-item w-full h-12 p-2 rounded-lg flex items-center justify-start space-x-2 transition text-gray-500 hover:bg-gray-200 hover:text-gray-700"
          type="button"
          on:click={logout}
        >
          <i class="icon-settings"></i>
          <span class="font-semibold">Logout</span>
        </button>
      </Link>
    </div>
  </div>
</div>
