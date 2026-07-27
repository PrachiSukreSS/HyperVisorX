import { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import api from "../services/api";

function Snapshots() {

      const [snapshotName, setSnapshotName] = useState("");
      const [showModal, setShowModal] = useState(false);

      const [snapshots, setSnapshots] = useState([]);
      const [loading, setLoading] = useState(true);

      useEffect(() => {
            loadSnapshots();
      }, []);

      async function loadSnapshots() {
            try {
                  const res = await api.get("/vms/rhel-control/snapshots");

                  console.log(res.data);

                  setSnapshots(res.data);

            } catch (err) {
                  console.error(err);
            } finally {
                  setLoading(false);
            }
      }

      async function restoreSnapshot(snapshotName) {
            try {

                  await api.post(
                        `/vms/rhel-control/snapshot/${snapshotName}/restore`
                  );

                  alert(`Snapshot '${snapshotName}' restored successfully.`);

            } catch (err) {

                  console.error(err);

                  alert("Failed to restore snapshot.");

            }
      }

      async function deleteSnapshot(snapshotName) {

            const confirmDelete = window.confirm(
                  `Delete snapshot '${snapshotName}'?`
            );

            if (!confirmDelete) return;

            try {

                  await api.delete(
                        `/vms/rhel-control/snapshot/${snapshotName}`
                  );

                  alert("Snapshot deleted successfully.");

                  loadSnapshots();

            } catch (err) {

                  console.error(err);

                  alert("Failed to delete snapshot.");

            }

      }

      async function createSnapshot() {

            if (!snapshotName.trim()) {

                  alert("Please enter a snapshot name.");

                  return;
            }

            try {

                  await api.post(
                        `/vms/rhel-control/snapshot/${snapshotName}`
                  );

                  alert("Snapshot created successfully.");

                  setSnapshotName("");

                  setShowModal(false);

                  loadSnapshots();

            } catch (err) {

                  console.error(err);

                  alert("Failed to create snapshot.");

            }

      }

      return (
            <div className="min-h-screen bg-slate-950 text-white">

                  <Navbar />

                  <div className="flex">

                        <Sidebar />

                        <main className="flex-1 p-8">

                              {/* Page Heading */}
                              <h1 className="text-3xl font-bold">
                                    VM Snapshots
                              </h1>

                              <p className="text-gray-400 mt-2">
                                    Create, Restore and Delete Virtual Machine Snapshots
                              </p>

                              {/* Snapshot Management Card */}
                              <div className="mt-8 bg-slate-900 rounded-xl border border-slate-700 p-6">

                                    <div className="flex justify-between items-center">

                                          <div>
                                                <h2 className="text-xl font-semibold">
                                                      Snapshot Management
                                                </h2>

                                                <p className="text-gray-400 mt-2">
                                                      Manage snapshots of your virtual machine.
                                                </p>
                                          </div>
                                          <button
                                                onClick={() => setShowModal(true)}
                                                className="
      bg-cyan-600
      hover:bg-cyan-500
      px-5
      py-2
      rounded-lg
      font-semibold
      transition
      "
                                          >
                                                + Create Snapshot
                                          </button>
                                    </div>

                                    {/* Snapshot Table */}

                                    <div className="mt-8 overflow-x-auto">

                                          <table className="w-full border-collapse">

                                                <thead>

                                                      <tr className="border-b border-slate-700 text-left">

                                                            <th className="py-3">
                                                                  Snapshot Name
                                                            </th>

                                                            <th className="py-3">
                                                                  Status
                                                            </th>

                                                            <th className="py-3">
                                                                  Created
                                                            </th>

                                                            <th className="py-3 text-center">
                                                                  Actions
                                                            </th>

                                                      </tr>

                                                </thead>

                                                <tbody>

                                                      {
                                                            loading ? (

                                                                  <tr>
                                                                        <td
                                                                              colSpan="4"
                                                                              className="py-6 text-center text-gray-400"
                                                                        >
                                                                              Loading snapshots...
                                                                        </td>
                                                                  </tr>

                                                            ) : snapshots.length === 0 ? (

                                                                  <tr>
                                                                        <td
                                                                              colSpan="4"
                                                                              className="py-6 text-center text-gray-400"
                                                                        >
                                                                              No snapshots found.
                                                                        </td>
                                                                  </tr>

                                                            ) : (

                                                                  snapshots.map((snapshot) => (

                                                                        <tr
                                                                              key={snapshot.name}
                                                                              className="border-b border-slate-800"
                                                                        >

                                                                              <td className="py-4">
                                                                                    {snapshot.name}
                                                                              </td>

                                                                              <td>
                                                                                    <span className="bg-green-600 px-3 py-1 rounded-full text-sm">
                                                                                          Available
                                                                                    </span>
                                                                              </td>

                                                                              <td>
                                                                                    QCOW2 Snapshot
                                                                              </td>

                                                                              <td className="text-center space-x-3">

                                                                                    <button
                                                                                          onClick={() => restoreSnapshot(snapshot.name)}
                                                                                          className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded-lg"
                                                                                    >
                                                                                          Restore
                                                                                    </button>

                                                                                    <button
                                                                                          onClick={() => deleteSnapshot(snapshot.name)}
                                                                                          className="bg-red-600 hover:bg-red-500 px-4 py-2 rounded-lg"
                                                                                    >
                                                                                          Delete
                                                                                    </button>

                                                                              </td>

                                                                        </tr>

                                                                  ))

                                                            )
                                                      }

                                                </tbody>
                                          </table>

                                    </div>

                              </div>

                        </main>

                  </div>
                  {
                        showModal && (

                              <div className="fixed inset-0 bg-black/60 flex items-center justify-center">

                                    <div className="bg-slate-900 p-6 rounded-xl w-96 border border-slate-700">

                                          <h2 className="text-xl font-semibold">
                                                Create Snapshot
                                          </h2>

                                          <input
                                                type="text"
                                                value={snapshotName}
                                                onChange={(e) => setSnapshotName(e.target.value)}
                                                placeholder="Enter Snapshot Name"
                                                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white"
                                          />

                                          <div className="flex justify-end gap-3 mt-6">

                                                <button
                                                      onClick={() => setShowModal(false)}
                                                      className="
                                    px-4
                                    py-2
                                    rounded-lg
                                    bg-gray-600
                                    hover:bg-gray-500
                                    "
                                                >
                                                      Cancel
                                                </button>

                                                <button
                                                      onClick={createSnapshot}
                                                      className="bg-cyan-600 hover:bg-cyan-500 px-5 py-2 rounded-lg"
                                                >
                                                      Create Snapshot
                                                </button>

                                          </div>

                                    </div>

                              </div>

                        )
                  }

            </div>

      );
}

export default Snapshots;