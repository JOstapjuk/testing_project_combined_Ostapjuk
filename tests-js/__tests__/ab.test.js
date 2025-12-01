const {
  VARIANDID,
  valiVariant,
  vahetaVariant,
  looLayoutHTML,
  looSyndmuseKeha,
} = require("../../frontend/ab.js");

describe("A/B loogika", () => {

  // Mock localStorage
  beforeAll(() => {
    global.localStorage = {
      getItem: jest.fn(() => null),  // Simulate empty localStorage (returns null)
      setItem: jest.fn(),  // Track calls to setItem
    };
  });

  test("valiVariant tagastab olemasoleva variandi", () => {
    const tulemus = valiVariant("variant_b", { sessioonId: "sess-1" });
    expect(tulemus.variant).toBe("variant_b");
    expect(tulemus.sessioonId).toBe("sess-1");
  });

  test("valiVariant kasutab juhuarvu deterministlikult", () => {
    const tulemus = valiVariant(null, { juhuarv: () => 0.99 });
    expect(VARIANDID).toContain(tulemus.variant);
  });

  test("vahetaVariant annab teise variandi", () => {
    expect(vahetaVariant("variant_a")).toBe("variant_b");
    expect(vahetaVariant("variant_b")).toBe("variant_a");
  });

  test("looLayoutHTML sisaldab variandi märksõnu", () => {
    expect(looLayoutHTML("variant_a")).toContain("Variant A");
    expect(looLayoutHTML("variant_b")).toContain("Variant B");
  });

  test("looSyndmuseKeha lisab metaandmed", () => {
    const keha = looSyndmuseKeha("variant_a", "katse", { sessioonId: "sess" });
    expect(keha.variant).toBe("variant_a");
    expect(keha.katsestaadium).toBe("katse");
    expect(keha.sessioonId).toBe("sess");
  });
});
