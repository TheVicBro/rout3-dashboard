<script lang="ts">
  import { QueryClientProvider } from '@tanstack/svelte-query'
  import { queryClient } from '$lib/queryClient';
  import { Router, Route, navigate } from 'svelte-routing';
  import { isAuthenticated } from './stores/auth';
  import { ModeWatcher } from "mode-watcher";
  import Layout from './components/Layout.svelte';
  import Secrets from './pages/Secrets.svelte';
  import Analytics from './pages/Analytics.svelte';
  import Billing from './pages/Billing.svelte';
  import Settings from './pages/Settings.svelte';
  import Account from './pages/Account.svelte';
  import Login from './pages/Login.svelte';
  import Configuration from './pages/Configuration.svelte';
  import MyAPI from './pages/MyAPI.svelte';
  import Chat from './pages/Chat.svelte';
  import Landing from './pages/Landing.svelte';
  import NotFound from './pages/404.svelte';
  
  import { Button } from "$lib/components/ui/button/index.js";

  function handleLoginSuccess() {
    navigate('/myapi');
  }
</script>

<QueryClientProvider client={queryClient}>
  <ModeWatcher />

  <Router>
    {#if $isAuthenticated}
      <Layout>
        <Route path="/chat" component={Chat} />
        <Route path="/myapi" component={MyAPI} />
        <Route path="/configuration" component={Configuration} />
        <Route path="/secrets" component={Secrets} />
        <Route path="/analytics" component={Analytics} />
        <Route path="/billing" component={Billing} />
        <Route path="/account" component={Account} />
        <Route path="/settings" component={Settings} />
        <Route path="*" component={NotFound} />
      </Layout>
    {:else}
      <Route path="/login">
        <div class="h-screen flex items-center justify-center bg-slate-100 dark:bg-slate-800">
          <div class="w-full px-6 py-8">
            <Login on:loginSuccess={handleLoginSuccess} />
          </div>
        </div>
      </Route>
      <Route path="/" component={Landing} />
      <Route path="*" component={NotFound} />
    {/if}
  </Router>
</QueryClientProvider>