
import { render, screen, cleanup } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import App from "./App";

// Clean the DOM after every test.
afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("PyCoin application", () => {
  it("renders the application title", () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => new Promise(() => {}))
    );

    render(<App />);

    const heading = screen.getByRole("heading", {
      name: "Welcome to PyCoin",
    });

    expect(heading).toBeTruthy();
  });

  it("displays cryptocurrency information", () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => new Promise(() => {}))
    );

    render(<App />);

    expect(screen.getByText("PYC")).toBeTruthy();

    expect(
      screen.getByText("Proof of Work")
    ).toBeTruthy();

    expect(
      screen.getByText("PyCoin", { selector: "strong" })
    ).toBeTruthy();
  });
});
