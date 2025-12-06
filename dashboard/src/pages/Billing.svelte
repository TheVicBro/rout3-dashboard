<script>
  import chartjs from 'chart.js/auto'
	import { onMount } from 'svelte';

	let chartValues = [50, 10, 5, 6];
	let chartLabels = ['OpenAI', 'Gemini', 'Mistral', 'Llama2'];
	let ctx;
	/**
	 * @type {{ getContext: (arg0: string) => any; }}
	 */
	let chartCanvas;

	onMount(async () => {
		  ctx = chartCanvas.getContext('2d');
			var chart = new chartjs(ctx, {
				type: 'doughnut',
				data: {
						labels: chartLabels,
						datasets: [{
								label: 'Cost',
								backgroundColor: ['rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 205, 86)', 'rgb(30, 64, 175)'],
								data: chartValues,
						}],
				},
        options: {
          responsive: true,
          maintainAspectRatio: false,
        }
		});

	});
</script>

<div class="flex flex-col min-h-screen">
  <h1 class="p-8 text-3xl font-bold bg-white dark:bg-slate-900 border-b dark:border-slate-800">Billing</h1>
  <div class="m-10 bg-white dark:bg-slate-900 rounded-lg border dark:border-slate-800 shadow-sm flex-1 overflow-hidden">
    <h2 class="p-8 text-xl font-semibold border-b dark:border-slate-800">Cost Breakdown</h2>
    <div class="p-8 flex-1 flex justify-center items-center">
      <div class="relative w-full max-w-4xl" style="height: calc(50vh - 100px);"> 
          <canvas bind:this={chartCanvas} id="myChart" class="absolute top-0 left-0 w-full h-full"></canvas>
      </div>
    </div>
    <div class="pt-4 px-4 flex justify-center text-center text-base text-slate-500">
      Monitor payouts, change payout methods, and manage your account through Stripe.
    </div>
    <div class="flex justify-center p-4 mb-4">
      <div class="bg-blue-800 text-white rounded-lg flex items-center cursor-pointer hover:bg-blue-700 transition p-4 px-32 bg-gradient-to-r from-blue-800 via-indigo-400 to-primary">
        <span class="flex items-center space-x-1 text-xl font-bold">
          <span>Visit</span>
          <img src="/stripe.svg" class="h-8" alt="Stripe Logo">
          <span>Dashboard</span>
        </span>
      </div>
    </div>
  </div>
</div>
