<script lang="ts">
  import { QueryClientProvider, QueryClient } from '@tanstack/svelte-query'
  import { Router, Route, navigate } from 'svelte-routing';
  import Sidebar from './components/Sidebar.svelte';
  import Secrets from './components/Secrets.svelte';
  import Analytics from './components/Analytics.svelte';
  import Billing from './components/Billing.svelte';
  import Settings from './components/Settings.svelte';
  import Account from './components/Account.svelte';
  import Login from './components/Login.svelte';
  import MyAI from './components/MyAI.svelte';
  import { isAuthenticated } from './stores/auth';
  import { onMount } from 'svelte';

  onMount(() => {
    // Check if the user is already authenticated on load
    if (localStorage.getItem("authToken")) {
      isAuthenticated.set(true);
    }
  });

  function handleLoginSuccess() {
    isAuthenticated.set(true);
    navigate('/secrets');
  }

  const queryClient = new QueryClient()
</script>

<QueryClientProvider client={queryClient}>
  {#if $isAuthenticated}
    <Router>
      <div class="flex h-screen bg-slate-100">
        <Sidebar />
        <div class="flex-1 flex flex-col overflow-hidden">
          <Route path="/myai" component={MyAI} />
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
    <div class="min-h-screen flex items-center justify-center bg-slate-100">
      <Login on:loginSuccess={handleLoginSuccess} />
    </div>
  {/if}
</QueryClientProvider>