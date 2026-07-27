import { useEffect, useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function Console() {
      const [consoleUrl, setConsoleUrl] = useState("");

      useEffect(() => {
            loadConsole();
      }, []);

      async function loadConsole() {
            try {
                  const res = await api.get("/console/rhel-control");

                  console.log("Console API Response:", res.data);
                  console.log("Console URL:", res.data.console_url);

                  // Backend returns: console_url
                  setConsoleUrl(res.data.console_url);

            } catch (err) {
                  console.error(err);
            }
      }

      return (
            <div className="min-h-screen bg-slate-950 text-white">
                  <Navbar />

                  <div className="flex">

                        <Sidebar />

                        <main className="flex-1 p-8">

                              <h1 className="text-3xl font-bold">
                                    VM Console
                              </h1>

                              <p className="text-gray-400 mt-2">
                                    Browser-based Virtual Machine Console
                              </p>

                              <div className="mt-8 rounded-xl overflow-hidden border border-slate-700">

                                    {consoleUrl ? (

                                          <iframe
                                                title="VM Console"
                                                src={consoleUrl}
                                                className="w-full"
                                                style={{
                                                      height: "80vh",
                                                      border: "none"
                                                }}
                                          />

                                    ) : (

                                          <div className="p-10">
                                                Loading Console...
                                          </div>

                                    )}

                              </div>

                        </main>

                  </div>

            </div>
      );
}

export default Console;