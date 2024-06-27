import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

const Analytics: React.FC = () => {
  const chartCanvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (chartCanvasRef.current) {
      const ctx = chartCanvasRef.current.getContext('2d');
      if (ctx) {
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            datasets: [{
              label: 'Revenue',
              backgroundColor: 'rgb(30, 64, 175)',
              borderColor: 'rgb(30, 64, 175)',
              data: [10, 10, 5, 2, 20, 30, 45, 50, 60, 70, 80, 90],
            }],
          },
          options: {
            responsive: true,
            maintainAspectRatio: true,
          },
        });
      }
    }
  }, []);

  return (
    <div className="flex flex-col min-h-screen">
      <h1 className="p-8 pl-20 text-3xl font-bold bg-white border-b-2">Analytics</h1>
      <div className="m-10 border rounded-lg bg-white shadow flex-1 overflow-hidden">
        <h2 className="p-10 pb-4 leading-none text-2xl font-semibold border-b-2">Overview</h2>
        <div className="p-10 pt-4">
          <div className="chart mt-4 flex space-x-1">
            <div className="w-full max-w-4xl mx-auto">
              <div className="relative">
                <canvas ref={chartCanvasRef} id="myChart" className="absolute top-0 left-0"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
