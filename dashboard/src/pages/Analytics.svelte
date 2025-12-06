<script>
  import chartjs from 'chart.js/auto'
	import { onMount } from 'svelte';

	let chartValues = [10, 10, 5, 2, 20, 30, 45, 50, 60, 70, 80, 90];
	let chartLabels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
	let ctx;
	/**
	 * @type {{ getContext: (arg0: string) => any; }}
	 */
	let chartCanvas;

	onMount(async () => {
		  ctx = chartCanvas.getContext('2d');
			var chart = new chartjs(ctx, {
				type: 'bar',
				data: {
						labels: chartLabels,
						datasets: [{
								label: 'Revenue',
								backgroundColor: 'rgb(30, 64, 175)',
								borderColor: 'rgb(30, 64, 175)',
								data: chartValues
						}]
				},
        options: {
          responsive: true,
          maintainAspectRatio: true,
        }
		});

	});
</script>

<div class="flex flex-col min-h-screen">
  <h1 class="p-8 text-3xl font-bold font-bold bg-white dark:bg-slate-900 border-b dark:border-slate-800">Analytics</h1>
  <div class="m-10 bg-white dark:bg-slate-900 rounded-lg border dark:border-slate-800 shadow-sm flex-1 overflow-hidden">
    <h2 class="p-8 text-xl font-semibold border-b dark:border-slate-800">Revenue Overview</h2>
    <div class="p-8">
      <div class="w-full max-w-5xl mx-auto h-[500px] relative">
        <canvas bind:this={chartCanvas} id="myChart"></canvas>
      </div>
    </div>
  </div>
</div>
