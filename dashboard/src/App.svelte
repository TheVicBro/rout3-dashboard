<script lang="ts">
  import { QueryClientProvider, QueryClient } from '@tanstack/svelte-query'
  import { Router, Route, navigate } from 'svelte-routing';
  import Sidebar from './components/Sidebar.svelte';
  import Secrets from './pages/Secrets.svelte';
  import Analytics from './pages/Analytics.svelte';
  import Billing from './pages/Billing.svelte';
  import Settings from './pages/Settings.svelte';
  import Account from './pages/Account.svelte';
  import Login from './pages/Login.svelte';
  import Configuration from './pages/Configuration.svelte';
  import MyAPI from './pages/MyAPI.svelte';
  import { isAuthenticated } from './stores/auth';
  import { onMount } from 'svelte';

  const queryClient = new QueryClient()

  onMount(() => {
    if (localStorage.getItem("authToken")) {
      isAuthenticated.set(true);
    }
  });

  function handleLoginSuccess() {
    isAuthenticated.set(true);
    navigate('/secrets');
  }
</script>

<QueryClientProvider client={queryClient}>
  {#if $isAuthenticated}
    <Router>
      <div class="flex h-screen bg-slate-100">
        <Sidebar />
        <div class="flex-1 flex flex-col overflow-hidden">
          <Route path="/myapi" component={MyAPI} />
          <Route path="/configuration" component={Configuration} />
          <Route path="/secrets" component={Secrets} />
          <Route path="/analytics" component={Analytics} />
          <Route path="/billing" component={Billing} />
          <Route path="/account" component={Account} />
          <Route path="/settings" component={Settings} />
          <Route path="/" component={Secrets} />
        </div>
      </div>
    </Router>
  {:else}
    <div class="h-screen flex items-center justify-center bg-slate-100">
      <div class="w-full px-6 py-8">
        <Login on:loginSuccess={handleLoginSuccess} />
      </div>
    </div>
  {/if}
</QueryClientProvider>