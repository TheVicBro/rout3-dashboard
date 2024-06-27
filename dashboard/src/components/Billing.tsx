import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

const Billing: React.FC = () => {
  const chartCanvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (chartCanvasRef.current) {
      const ctx = chartCanvasRef.current.getContext('2d');
      if (ctx) {
        new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: ['OpenAI', 'Gemini', 'Mistral', 'Llama2'],
            datasets: [{
              label: 'Cost',
              backgroundColor: ['rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 205, 86)', 'rgb(30, 64, 175)'],
              data: [50, 10, 5, 6],
            }],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
          },
        });
      }
    }
  }, []);

  return (
    <div className="flex flex-col min-h-screen">
      <h1 className="p-8 pl-20 text-3xl font-bold bg-white border-b-2">Billing</h1>
      <div className="m-10 border rounded-lg bg-white shadow flex-1 overflow-hidden">
        <h2 className="p-10 pb-4 leading-none text-2xl font-semibold border-b-2">Overview</h2>
        <div className="p-4 pt-8 flex-1 flex justify-center items-center">
          <div className="relative w-full max-w-4xl" style={{ height: 'calc(50vh - 100px)' }}>
            <canvas ref={chartCanvasRef} id="myChart" className="absolute top-0 left-0 w-full h-full"></canvas>
          </div>
        </div>
        <div className="pt-4 px-4 flex justify-center text-center text-base text-slate-500">
          Monitor payouts, change payout methods, and manage your account through Stripe.
        </div>
        <div className="flex justify-center p-4 mb-4">
          <div className="bg-blue-800 text-white rounded-lg flex items-center cursor-pointer hover:bg-blue-700 transition p-4 px-32 bg-gradient-to-r from-blue-800 via-indigo-400 to-primary">
            <span className="flex items-center space-x-1 text-xl font-bold">
              <span>Visit</span>
              <img src="/stripe.svg" className="h-8" alt="Stripe Logo" />
              <span>Dashboard</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Billing;
