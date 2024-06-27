import React, { useState } from 'react';

const modelProviders = ["OpenAI", "Hugging Face", "Google AI", "Microsoft Azure"];

const MyAI: React.FC = () => {
  const [selectedModel, setSelectedModel] = useState(modelProviders[0]);
  const [temperature, setTemperature] = useState(0.7);
  const [maxTokens, setMaxTokens] = useState(100);
  const [guardRails, setGuardRails] = useState<string[]>([""]);

  const setupModel = () => {
    alert(`Model from ${selectedModel} set up with temperature ${temperature} and max tokens ${maxTokens}.`);
    document.getElementById('model-iframe')!.style.display = 'block';
  };

  const addGuardRail = () => {
    setGuardRails([...guardRails, ""]);
  };

  const updateGuardRail = (index: number, value: string) => {
    const newGuardRails = [...guardRails];
    newGuardRails[index] = value;
    setGuardRails(newGuardRails);
  };

  const removeGuardRail = (index: number) => {
    const newGuardRails = guardRails.filter((_, i) => i !== index);
    setGuardRails(newGuardRails);
  };

  return (
    <div className="flex flex-col flex-1">
      <h1 className="p-8 pl-20 text-3xl font-bold bg-white border-b-2">MyAI</h1>
      <div className="m-10 border rounded-lg bg-white shadow flex-1 overflow-auto">
        <h2 className="p-10 pb-4 leading-none text-2xl font-semibold border-b-2">Overview</h2>
        <div className="p-20 px-64">
          <h3 className="text-xl font-semibold mb-4">Select a Model Provider</h3>
          <select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)} className="border p-2 rounded mb-4">
            {modelProviders.map(provider => (
              <option key={provider} value={provider}>{provider}</option>
            ))}
          </select>
          <h3 className="text-xl font-semibold mb-4">Model Settings</h3>
          <div className="mb-4">
            <label htmlFor="temperature" className="block font-semibold mb-1">Temperature</label>
            <input id="temperature" type="range" min="0" max="1" step="0.01" value={temperature} onChange={(e) => setTemperature(Number(e.target.value))} className="w-full" />
            <span>{temperature.toFixed(2)}</span>
          </div>
          <div className="mb-4">
            <label htmlFor="maxTokens" className="block font-semibold mb-1">Max Tokens</label>
            <input id="maxTokens" type="number" min="1" max="1000" value={maxTokens} onChange={(e) => setMaxTokens(Number(e.target.value))} className="w-full border p-2 rounded" />
          </div>
          <h3 className="text-xl font-semibold mb-4">Guard Rails</h3>
          {guardRails.map((guardRail, index) => (
            <div key={index} className="mb-4 flex items-center">
              <input
                type="text"
                className="w-full border p-2 rounded mb-2"
                placeholder="Add guard rail"
                value={guardRail}
                onChange={(e) => updateGuardRail(index, e.target.value)}
              />
              {index > 0 && (
                <button onClick={() => removeGuardRail(index)} className="ml-2 text-red-500 hover:text-red-700">Remove</button>
              )}
            </div>
          ))}
          <button onClick={addGuardRail} className="px-4 py-2 text-white rounded-lg bg-red-800 hover:bg-red-700 transition mb-4">Add Guard Rail</button>
          <button onClick={setupModel} className="px-4 py-2 text-white rounded-lg bg-blue-800 hover:bg-blue-700 transition">Set Up Model</button>
          <div id="model-iframe" style={{ display: 'none' }} className="mt-8 border rounded overflow-hidden">
            <iframe src="https://example.com" className="w-full h-96"></iframe>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MyAI;
