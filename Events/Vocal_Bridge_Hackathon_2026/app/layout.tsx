import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FinePrint",
  description: "Your insurance policy, actually readable.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body style={{ background: "#E8E9D6" }}>{children}</body>
    </html>
  );
}
