const VARIANDID = ["variant_a", "variant_b"];
const SALVESTUS_VOITME = "kvaliteedijalg_variant";

function looSessioonId() {
  return `sess-${Math.random().toString(36).slice(2, 10)}`;
}

function taastaVariant(salvesti) {
  const hoidla =
    salvesti || (typeof window !== "undefined" ? window.localStorage : null);
  if (!hoidla) {
    return null;
  }
  return hoidla.getItem(SALVESTUS_VOITME);
}

function salvestaVariant(variant, salvesti) {
  const hoidla =
    salvesti || (typeof window !== "undefined" ? window.localStorage : null);
  if (!hoidla) {
    return;
  }
  hoidla.setItem(SALVESTUS_VOITME, variant);
}

function valiVariant(soovitud, valikud = {}) {
  const { juhuarv = Math.random, eelmine = null, sessioonId = null } = valikud;
  
  const kasulik = VARIANDID.includes(soovitud || "")
    ? soovitud
    : VARIANDID.includes(eelmine || "")
    ? eelmine
    : VARIANDID[Math.floor(juhuarv() * VARIANDID.length)];

  // Save the selected variant to localStorage (or custom storage)
  salvestaVariant(kasulik); 

  return {
    variant: kasulik,
    sessioonId: sessioonId || looSessioonId(),
  };
}


function looLayoutHTML(variant) {
  if (variant === "variant_b") {
    return `
      <article class="variant-b">
        <h3>Variant B – visuaalne voog</h3>
        <p>Fookus on piltidel ja kiirel CTA-l.</p>
        <ul>
          <li>Heledam CTA nupp</li>
          <li>Piltide karussell</li>
          <li>Kasutaja lugude tsitaadid</li>
        </ul>
      </article>
    `;
  }

  return `
    <article class="variant-a">
      <h3>Variant A – tekstikeskne</h3>
      <p>Selgitab väärtuspakkumist üksikasjalikult.</p>
      <ul>
        <li>Struktureeritud kontrollnimekiri</li>
        <li>GA4 sündmuste selgitused</li>
        <li>Püsivad mõõdikud</li>
      </ul>
    </article>
  `;
}

function vahetaVariant(hetkene) {
  return hetkene === "variant_a" ? "variant_b" : "variant_a";
}

function looSyndmuseKeha(variant, staadium = "katse", lisa = {}) {
  return {
    event_category: "ab_test",
    event_label: variant,
    variant,
    katsestaadium: staadium,
    ...lisa,
  };
}

const ABTest = {
  VARIANDID,
  valiVariant,
  salvestaVariant,
  taastaVariant,
  looLayoutHTML,
  vahetaVariant,
  looSyndmuseKeha,
};

if (typeof window !== "undefined") {
  window.ABTest = ABTest;
}

if (typeof module !== "undefined") {
  module.exports = ABTest;
}

