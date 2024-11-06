<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { navigate } from "svelte-routing";
  import { isAuthenticated } from '../stores/auth';
  import { ArrowLeft } from 'lucide-svelte';

  // Determine where to navigate back to based on auth status
  function goBack() {
    if ($isAuthenticated) {
      navigate('/myapi');
    } else {
      navigate('/');
    }
  }
</script>

<div class="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-900">
  <div class="text-center px-4">
    <h1 class="text-9xl font-bold text-slate-900 dark:text-slate-100 mb-4">404</h1>
    <div class="relative">
      <div class="absolute -top-2 w-full">
        <div class="h-1 w-full bg-gradient-to-r from-blue-600 to-purple-600 rounded"></div>
      </div>
      <h2 class="text-3xl font-semibold text-slate-800 dark:text-slate-200 mb-6">Page Not Found</h2>
    </div>
    <p class="text-lg text-slate-600 dark:text-slate-400 mb-8 max-w-md mx-auto">
      The page you're looking for doesn't exist or has been moved.
    </p>
    <Button 
      on:click={goBack}
      class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-slate-100"
    >
      <ArrowLeft class="mr-2 h-4 w-4" />
      Go Back Home
    </Button>
  </div>
</div>