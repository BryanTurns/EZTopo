import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders the upload prompt", () => {
  render(<App />);
  expect(screen.getByRole("heading", { name: /eztopo/i })).toBeInTheDocument();
  expect(screen.getByText(/drop a video here/i)).toBeInTheDocument();
});
