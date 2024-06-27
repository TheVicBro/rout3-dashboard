// import { useQuery, useQueryClient } from '@tanstack/react-query';
// import { useState } from 'react';

// type Repo = {
//   name: string;
//   last_used: string | null;
//   user_id: number;
//   id: number;
//   key: string;
// };

// export default function Secrets() {
//   const queryClient = useQueryClient();
//   const token = localStorage.getItem("authToken");
//   const [addKeyPopup, setAddKeyPopup] = useState(false);
//   const [newName, setNewName] = useState('');
//   const [newKey, setNewKey] = useState('');
//   const [removeKeyPopup, setRemoveKeyPopup] = useState(false);
//   const [selectedSecretId, setSelectedSecretId] = useState<number | null>(null);

//   const fetchRepos = async (): Promise<Repo[]> => {
//     const response = await fetch('http://127.0.0.1:8000/secrets/list?user_id=1', {
//       method: 'GET',
//       headers: {
//         'Content-Type': 'application/json',
//         Authorization: `Basic ${token}`,
//       }
//     });
//     if (!response.ok) {
//       throw new Error(`Network response was not ok: ${response.statusText}`);
//     }
//     return response.json();
//   };

//   const { data, error, isLoading } = useQuery<Repo[]>('repoData', fetchRepos);

//   const addNewKey = async () => {
//     const response = await fetch('http://127.0.0.1:8000/secrets/create', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//         Authorization: `Basic ${token}`,
//       },
//       body: JSON.stringify({
//         name: newName,
//         key: newKey,
//       }),
//     });
//     if (!response.ok) {
//       throw new Error(`Network response was not ok: ${response.statusText}`);
//     }
//     queryClient.invalidateQueries('repoData');
//     setAddKeyPopup(false);
//   };

//   const removeKey = async () => {
//     const response = await fetch('http://127.0.0.1:8000/secrets/delete', {
//       method: 'DELETE',
//       headers: {
//         'Content-Type': 'application/json',
//         Authorization: `Basic ${token}`,
//       },
//       body: JSON.stringify({
//         secret_id: selectedSecretId,
//       }),
//     });
//     if (!response.ok) {
//       throw new Error(`Network response was not ok: ${response.statusText}`);
//     }
//     queryClient.invalidateQueries('repoData');
//     setRemoveKeyPopup(false);
//   };

//   return (
//     <div>
//       <h1 className="p-8 pl-20 text-3xl font-bold bg-white border-b-2">Secrets</h1>
//       <div className="m-10 border rounded-lg bg-white shadow">
//         <h2 className="p-10 pb-4 leading-none text-2xl font-semibold border-b-2">Overview</h2>
//         <div className="p-10">
//           {isLoading && <p>Loading...</p>}
//           {error && <p>An error has occurred: {(error as Error).message}</p>}
//           {data && (
//             <table className="w-full">
//               <thead>
//                 <tr>
//                   <th className="text-left p-2">Name</th>
//                   <th className="text-left p-2">Key</th>
//                   <th className="text-left p-2">Last Used</th>
//                 </tr>
//               </thead>
//               <tbody>
//                 {data.map((repo) => (
//                   <tr key={repo.id}>
//                     <td className="p-2">{repo.name}</td>
//                     <td className="p-2">{repo.key}</td>
//                     <td className="p-2">{repo.last_used}</td>
//                   </tr>
//                 ))}
//               </tbody>
//             </table>
//           )}
//         </div>
//       </div>
//       <button className="ml-10 px-8 py-2 bg-blue-800 transition hover:bg-blue-700 hover:transition text-white rounded-lg" onClick={() => setAddKeyPopup(true)}>+ Add a new key</button>
//       <button className="ml-10 px-8 py-2 bg-blue-800 transition hover:bg-blue-700 hover:transition text-white rounded-lg" onClick={() => setRemoveKeyPopup(true)}>+ Remove a key</button>

//       {addKeyPopup && (
//         <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
//           <div className="bg-white rounded-lg shadow-lg p-8 w-96 relative">
//             <button className="absolute pb-1 top-4 right-4 text-gray-500 hover:text-gray-700 text-4xl rounded-full h-12 w-12 flex items-center justify-center hover:bg-gray-200 transition duration-200 ease-in-out" onClick={() => setAddKeyPopup(false)}>
//               &times;
//             </button>
//             <h2 className="text-2xl font-semibold mb-4">Add New Key</h2>
//             <div className="space-y-4">
//               <div>
//                 <div className="block text-gray-700">Name</div>
//                 <input type="text" value={newName} onChange={(e) => setNewName(e.target.value)} className="form-input mt-1 block w-full border rounded p-2" />
//               </div>
//               <div>
//                 <div className="block text-gray-700">Key</div>
//                 <input type="text" value={newKey} onChange={(e) => setNewKey(e.target.value)} className="form-input mt-1 block w-full border rounded p-2" />
//               </div>
//               <div className="pt-6">
//                 <button className="px-4 py-2 bg-blue-800 text-white rounded-lg hover:bg-blue-700 focus:outline-none" onClick={addNewKey}>Add Key</button>
//               </div>
//             </div>
//           </div>
//         </div>
//       )}

//       {removeKeyPopup && (
//         <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
//           <div className="bg-white rounded-lg shadow-lg p-8 w-96 relative">
//             <button className="absolute pb-1 top-4 right-4 text-gray-500 hover:text-gray-700 text-4xl rounded-full h-12 w-12 flex items-center justify-center hover:bg-gray-200 transition duration-200 ease-in-out" onClick={() => setRemoveKeyPopup(false)}>
//               &times;
//             </button>
//             <h2 className="text-2xl font-semibold mb-4">Remove Key</h2>
//             <div className="space-y-4">
//               {data && (
//                 <div>
//                   <div className="block text-gray-700">Select Secret to Remove</div>
//                   <select value={selectedSecretId ?? ''} onChange={(e) => setSelectedSecretId(Number(e.target.value))} className="form-select mt-1 block w-full border rounded p-2">
//                     <option value="" disabled>Select a key</option>
//                     {data.map((repo) => (
//                       <option key={repo.id} value={repo.id}>{repo.name}</option>
//                     ))}
//                   </select>
//                 </div>
//               )}
//               <div className="pt-6">
//                 <button className="px-4 py-2 bg-blue-800 text-white rounded-lg hover:bg-blue-700 focus:outline-none" onClick={removeKey}>Remove Key</button>
//               </div>
//             </div>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }
