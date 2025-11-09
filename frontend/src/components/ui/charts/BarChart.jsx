import { BarChart, Bar, XAxis, Tooltip, ResponsiveContainer } from "recharts";

const data = [
  { name: "Jan", value: 30 },
  { name: "Feb", value: 20 },
  { name: "Mar", value: 45 },
  { name: "Apr", value: 35 },
  { name: "May", value: 50 },
];

export default function CustomBarChart() {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data}>
        <XAxis dataKey="name" />
        <Tooltip />
        <Bar dataKey="value" fill="#3B82F6" radius={[6, 6, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
