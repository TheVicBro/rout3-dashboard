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
  <h1 class="p-8 pl-20 text-3xl font-bold font-bold bg-white border-b-2">Analytics</h1>
  <div class="m-10 border rounded-lg bg-white shadow flex-1 overflow-hidden">
    <h2 class="p-10 pb-4 leading-none text-2xl font-semibold border-b-2">Overview</h2>
    <div class="p-10 pt-4">
      <div class="chart mt-4 flex space-x-1">
        <div class="w-full max-w-4xl mx-auto">
          <div class="relative "> 
            <canvas bind:this={chartCanvas} id="myChart" class="absolute top-0 left-0"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
