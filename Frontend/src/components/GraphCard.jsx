import {
      LineChart,
      Line,
      ResponsiveContainer,
      XAxis,
      YAxis,
      CartesianGrid,
      Tooltip,
} from "recharts";

function GraphCard({ title, data, dataKey }) {
      return (
            <div className="bg-slate-900 rounded-xl p-5 shadow-lg">
                  <h3 className="text-lg font-semibold mb-4">{title}</h3>

                  <ResponsiveContainer width="100%" height={250}>
                        <LineChart data={data}>
                              <CartesianGrid stroke="#333" />

                              <XAxis hide />

                              <YAxis />

                              <Tooltip />

                              <Line
                                    type="monotone"
                                    dataKey={dataKey}
                                    stroke="#38bdf8"
                                    strokeWidth={3}
                                    dot={false}
                              />
                        </LineChart>
                  </ResponsiveContainer>
            </div>
      );
}

export default GraphCard;