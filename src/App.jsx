import React, { useState } from 'react';

// ── Company data ──────────────────────────────────────────────────────────────

const COMPANIES = [
  {
    slug: 'google',
    name: 'Google',
    parent: 'Alphabet Inc.',
    ticker: 'GOOGL',
    tags: ['Cloud', 'Enterprise AI', 'Advertising'],
    accent: '#4285f4',
    grad: ['#4285f4', '#34a853'],
    logoBg: '#ffffff',          // white so the 4-color G shows correctly
    summary: 'Enterprise AI infrastructure, Cloud platform growth, and global search and YouTube at scale.',
  },
  {
    slug: 'apple',
    name: 'Apple',
    parent: 'Apple Inc.',
    ticker: 'AAPL',
    tags: ['Digital Health', 'Devices', 'ML Research'],
    accent: '#8e8e93',
    grad: ['#2c2c2e', '#48484a'],
    logoBg: null,               // use gradient
    summary: 'Integrated device ecosystem, ResearchKit, wearable health surfaces, and on-device intelligence.',
  },
  {
    slug: 'pfizer',
    name: 'Pfizer',
    parent: 'Pfizer Inc.',
    ticker: 'PFE',
    tags: ['Oncology', 'Vaccines', 'Clinical Trials'],
    accent: '#0093d0',
    grad: ['#0093d0', '#00617f'],
    logoBg: '#ffffff',          // white so wordmark shows in brand blue
    summary: 'Translational science, diversified late-stage pipeline, vaccine infrastructure, and clinical R&D.',
  },
  {
    slug: 'eli-lilly',
    name: 'Eli Lilly',
    parent: 'Eli Lilly and Company',
    ticker: 'LLY',
    tags: ['Cardiometabolic', 'Oncology', 'Neuroscience'],
    accent: '#C8102E',
    grad: ['#C8102E', '#8b0d1f'],
    logoBg: '#ffffff',          // white so wordmark shows in brand red
    summary: 'Blockbuster cardiometabolic franchise (Mounjaro, Zepbound) with deep pipeline across oncology, immunology, and neuroscience.',
  },
  {
    slug: 'jnj',
    name: 'Johnson & Johnson',
    parent: 'Johnson & Johnson',
    ticker: 'JNJ',
    tags: ['Innovative Medicine', 'MedTech', 'Clinical Trials'],
    accent: '#CC0000',
    grad: ['#CC0000', '#8B0000'],
    logoBg: '#ffffff',
    summary: 'Diversified healthcare leader spanning Innovative Medicine and MedTech with $94.2B FY2025 sales and AI-enabled clinical operations.',
  },
  {
    slug: 'microsoft',
    name: 'Microsoft',
    parent: 'Microsoft Corporation',
    ticker: 'MSFT',
    tags: ['Cloud', 'Enterprise AI', 'Health Data'],
    accent: '#0078D4',
    grad: ['#0078D4', '#005a9e'],
    logoBg: '#ffffff',
    summary: '$281.7B FY2025 revenue. Azure at $75B+. AI business at $37B run rate. FHIR health data infrastructure and 200+ AI for Health grantee partnerships.',
  },
  {
    slug: 'epic',
    name: 'Epic',
    parent: 'Epic Systems Corporation',
    ticker: 'Private',
    tags: ['EHR', 'Clinical AI', 'Cosmos'],
    accent: '#CC1230',
    grad: ['#CC1230', '#8a0d20'],
    logoBg: '#ffffff',
    summary: 'Dominant U.S. EHR (43.7% market share). Cosmos: 300M+ deidentified patient records. UNC Health is an active co-development partner with 3 documented AI milestones.',
  },
  {
    slug: 'unc-health',
    name: 'UNC Health',
    parent: 'UNC Health Care System',
    ticker: 'State Entity',
    tags: ['Academic Health System', 'SHIRE', 'NC TraCS'],
    accent: '#4B9CD3',
    grad: ['#13294B', '#4B9CD3'],
    logoBg: '#ffffff',
    summary: '$7.4B academic health system. 17 hospitals, 900+ clinics, 56K employees. SHIRE AI research platform live April 2026. NC Lineberger NCI Cancer Center. UNC\'s own clinical asset.',
  },
  {
    slug: 'duke-health',
    name: 'Duke Health',
    parent: 'Duke University Health System',
    ticker: 'Private',
    tags: ['Academic Health System', 'DCRI', 'Duke AI Health'],
    accent: '#001A57',
    grad: ['#001A57', '#003a8c'],
    logoBg: '#ffffff',
    summary: '$7B+ academic health system. 4 hospitals, 140+ clinics, 26K employees. Home of DCRI (world\'s largest academic CRO). Triangle peer to UNC Health via Carolinas Collaborative.',
  },
  {
    slug: 'atrium-health',
    name: 'Atrium Health',
    parent: 'Advocate Health',
    ticker: 'NC Authority',
    tags: ['Largest NC System', 'The Pearl', 'Wake Forest SOM'],
    accent: '#00833D',
    grad: ['#00833D', '#006830'],
    logoBg: '#ffffff',
    summary: '$14.5B Charlotte/GA operations within Advocate Health ($38.9B). 40 hospitals, 500+ care locations. The Pearl innovation district opened June 2025. Proposed WakeMed combination May 2026.',
  },
  {
    slug: 'siemens-healthineers',
    name: 'Siemens Healthineers',
    parent: 'Siemens Healthineers AG',
    ticker: 'FWB: SHL',
    tags: ['Imaging', 'Varian / Radiation Oncology', 'Value Partnerships'],
    accent: '#009B9E',
    grad: ['#009B9E', '#006E72'],
    logoBg: null,            // teal gradient background shows the white-S circle mark
    summary: '€23.4B MedTech leader. Varian radiation oncology platform. teamplay AI on 5,000+ institutions. $141M committed to The Pearl NC. 200+ Value Partnerships with academic health systems.',
  },
];

function hexRgb(hex) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `${r},${g},${b}`;
}

function filterCompanies(query) {
  const q = query.toLowerCase().replace(/[^a-z0-9]/g, '');
  if (!q) return COMPANIES;
  return COMPANIES.filter(c =>
    [c.name, c.parent, c.ticker, ...c.tags].some(s =>
      s.toLowerCase().replace(/[^a-z0-9]/g, '').includes(q)
    )
  );
}

// ── Company logo SVGs ─────────────────────────────────────────────────────────

function GoogleLogo({ size }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
      <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
      <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
      <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
    </svg>
  );
}

function AppleLogo({ size, color = '#fff' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill={color} xmlns="http://www.w3.org/2000/svg">
      <path d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.54 9.103 1.519 12.09 1.013 1.459 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/>
    </svg>
  );
}

// Pfizer — wordmark "pfizer" in brand blue on white background.
// viewBox matches display size so fontSize scales correctly at every size.
function PfizerLogo({ size }) {
  const fs = Math.round(size * 0.28);   // 6 chars: fits width at 0.28×
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}
         xmlns="http://www.w3.org/2000/svg" overflow="visible">
      <text
        x={size / 2} y={size * 0.63}
        textAnchor="middle"
        fontFamily="'Helvetica Neue', Helvetica, Arial, sans-serif"
        fontSize={fs}
        fontWeight="700"
        fill="#0093d0"
        letterSpacing="-0.3"
      >pfizer</text>
    </svg>
  );
}

// Eli Lilly — wordmark "Lilly" in brand red on white background.
function LillyLogo({ size }) {
  const fs = Math.round(size * 0.32);   // 5 chars: fits width at 0.32×
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}
         xmlns="http://www.w3.org/2000/svg" overflow="visible">
      <text
        x={size / 2} y={size * 0.64}
        textAnchor="middle"
        fontFamily="'Helvetica Neue', Helvetica, Arial, sans-serif"
        fontSize={fs}
        fontWeight="700"
        fill="#C8102E"
        letterSpacing="-0.2"
      >Lilly</text>
    </svg>
  );
}

// Epic Systems — bold italic "Epic" wordmark in brand red, matching official logo.
function EpicLogo({ size }) {
  const fs = Math.round(size * 0.36);
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}
         xmlns="http://www.w3.org/2000/svg" overflow="visible">
      <text
        x={size / 2} y={size * 0.66}
        textAnchor="middle"
        fontFamily="'Helvetica Neue', Helvetica, Arial, sans-serif"
        fontSize={fs}
        fontWeight="800"
        fontStyle="italic"
        fill="#CC1230"
        letterSpacing="-0.5"
      >Epic</text>
    </svg>
  );
}

// UNC Health — two-tone "UNC / Health" wordmark in navy + Carolina blue.
function UNCHealthLogo({ size }) {
  const fs1 = Math.round(size * 0.30);   // "UNC" — larger
  const fs2 = Math.round(size * 0.19);   // "Health" — smaller below
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}
         xmlns="http://www.w3.org/2000/svg" overflow="visible">
      <text x={size / 2} y={size * 0.46}
        textAnchor="middle"
        fontFamily="'Helvetica Neue', Helvetica, Arial, sans-serif"
        fontSize={fs1} fontWeight="800" fill="#13294B"
        letterSpacing="-0.5">UNC</text>
      <text x={size / 2} y={size * 0.68}
        textAnchor="middle"
        fontFamily="'Helvetica Neue', Helvetica, Arial, sans-serif"
        fontSize={fs2} fontWeight="600" fill="#4B9CD3"
        letterSpacing="0.5">Health</text>
    </svg>
  );
}

// Duke Health — bold "Duke" wordmark with "HEALTH" beneath in Duke navy.
function DukeHealthLogo({ size }) {
  const fs1 = Math.round(size * 0.34);
  const fs2 = Math.round(size * 0.16);
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}
         xmlns="http://www.w3.org/2000/svg" overflow="visible">
      <text x={size/2} y={size*0.50} textAnchor="middle"
        fontFamily="'Helvetica Neue', Helvetica, Arial, sans-serif"
        fontSize={fs1} fontWeight="800" fill="#001A57"
        letterSpacing="-0.5">Duke</text>
      <text x={size/2} y={size*0.72} textAnchor="middle"
        fontFamily="'Helvetica Neue', Helvetica, Arial, sans-serif"
        fontSize={fs2} fontWeight="700" fill="#003a8c"
        letterSpacing="2">HEALTH</text>
    </svg>
  );
}

// Atrium Health — bold "Atrium" wordmark in green with "HEALTH" beneath.
function AtriumHealthLogo({ size }) {
  const fs1 = Math.round(size * 0.28);
  const fs2 = Math.round(size * 0.16);
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}
         xmlns="http://www.w3.org/2000/svg" overflow="visible">
      <text x={size/2} y={size*0.50} textAnchor="middle"
        fontFamily="'Helvetica Neue', Helvetica, Arial, sans-serif"
        fontSize={fs1} fontWeight="800" fill="#00833D"
        letterSpacing="-0.5">Atrium</text>
      <text x={size/2} y={size*0.72} textAnchor="middle"
        fontFamily="'Helvetica Neue', Helvetica, Arial, sans-serif"
        fontSize={fs2} fontWeight="700" fill="#006830"
        letterSpacing="2">HEALTH</text>
    </svg>
  );
}


// Siemens Healthineers — white "S" only; teal gradient avatar bg provides the circle.
function SiemensHealthineersLogo({ size }) {
  const fs = Math.round(size * 0.68);
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}
         xmlns="http://www.w3.org/2000/svg">
      <text x={size / 2} y={size * 0.73}
        textAnchor="middle"
        fontFamily="'Helvetica Neue', Helvetica, Arial, sans-serif"
        fontSize={fs} fontWeight="700" fill="white"
        letterSpacing="-1">S</text>
    </svg>
  );
}

// Microsoft — official 4-square Windows flag logo.
function MicrosoftLogo({ size }) {
  const gap = size * 0.06;
  const sq  = (size - gap) / 2;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} xmlns="http://www.w3.org/2000/svg">
      {/* Top-left: red */}
      <rect x={0}        y={0}        width={sq} height={sq} fill="#F25022"/>
      {/* Top-right: green */}
      <rect x={sq+gap}   y={0}        width={sq} height={sq} fill="#7FBA00"/>
      {/* Bottom-left: blue */}
      <rect x={0}        y={sq+gap}   width={sq} height={sq} fill="#00A4EF"/>
      {/* Bottom-right: yellow */}
      <rect x={sq+gap}   y={sq+gap}   width={sq} height={sq} fill="#FFB900"/>
    </svg>
  );
}

// Johnson & Johnson — classic red script wordmark rendered as two-line italic serif text.
function JNJLogo({ size }) {
  const fs = Math.round(size * 0.185);  // two lines of "Johnson" fit at ~0.185×
  const y1 = size * 0.44;
  const y2 = size * 0.70;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}
         xmlns="http://www.w3.org/2000/svg" overflow="visible">
      <text
        x={size / 2} y={y1}
        textAnchor="middle"
        fontFamily="Georgia, 'Times New Roman', serif"
        fontSize={fs}
        fontStyle="italic"
        fontWeight="400"
        fill="#CC0000"
      >Johnson</text>
      <text
        x={size / 2} y={y2}
        textAnchor="middle"
        fontFamily="Georgia, 'Times New Roman', serif"
        fontSize={fs}
        fontStyle="italic"
        fontWeight="400"
        fill="#CC0000"
      >&amp; Johnson</text>
    </svg>
  );
}

function CompanyLogo({ slug, size }) {
  if (slug === 'google')    return <GoogleLogo size={size} />;
  if (slug === 'apple')     return <AppleLogo size={size} color="#fff" />;
  if (slug === 'pfizer')    return <PfizerLogo size={size} />;
  if (slug === 'eli-lilly') return <LillyLogo size={size} />;
  if (slug === 'jnj')       return <JNJLogo size={size} />;
  if (slug === 'microsoft') return <MicrosoftLogo size={size} />;
  if (slug === 'epic')       return <EpicLogo size={size} />;
  if (slug === 'unc-health') return <UNCHealthLogo size={size} />;
  if (slug === 'duke-health') return <DukeHealthLogo size={size} />;
  if (slug === 'atrium-health') return <AtriumHealthLogo size={size} />;
  if (slug === 'siemens-healthineers') return <SiemensHealthineersLogo size={size} />;
  return null;
}

// ── Avatar container ──────────────────────────────────────────────────────────
// Google gets white bg so the 4-color G shows; others use their gradient.

function Avatar({ co, size, shadow = false }) {
  const hasWhiteBg = co.logoBg === '#ffffff';
  // Google's colorful G needs more room; wordmarks need slightly more too
  const logoSize = Math.round(size * (hasWhiteBg ? 0.78 : 0.62));

  return (
    <div style={{
      width: size, height: size,
      borderRadius: Math.round(size * 0.27),
      background: co.logoBg ?? `linear-gradient(135deg, ${co.grad[0]}, ${co.grad[1]})`,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      flexShrink: 0,
      boxShadow: shadow ? `0 4px 20px rgba(${hexRgb(co.accent)},0.35)` : 'none',
      transition: 'box-shadow 0.2s ease',
      border: hasWhiteBg ? '1px solid #e8e8e8' : 'none',
      pointerEvents: 'none',   // SVG logos must not capture clicks — parent button handles them
    }}>
      <CompanyLogo slug={co.slug} size={logoSize} />
    </div>
  );
}

// ── Icons ─────────────────────────────────────────────────────────────────────

const IconSearch = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#52525b" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
  </svg>
);

const IconDownload = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
    <polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
  </svg>
);

const IconChevron = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="9 18 15 12 9 6"/>
  </svg>
);

// ── Sidebar company card ──────────────────────────────────────────────────────

function CompanyCard({ co, selected, onSelect }) {
  const [hov, setHov] = useState(false);
  const active = selected === co.slug;

  return (
    <button
      onClick={onSelect}
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
      style={{
        display: 'flex', alignItems: 'center', gap: '11px',
        width: '100%', padding: '11px 14px',
        background: active ? `rgba(${hexRgb(co.accent)},0.08)` : hov ? 'rgba(255,255,255,0.04)' : 'transparent',
        border: 'none',
        borderLeft: `2px solid ${active ? co.accent : 'transparent'}`,
        borderRadius: '0 10px 10px 0',
        cursor: 'pointer', textAlign: 'left',
        transition: 'all 0.15s ease',
        marginBottom: '3px',
      }}
    >
      <Avatar co={co} size={34} />

      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{
          fontSize: '13px', fontWeight: active ? '600' : '500',
          color: active ? '#f4f4f5' : hov ? '#d4d4d8' : '#a1a1aa',
          letterSpacing: '-0.01em', marginBottom: '2px',
          transition: 'color 0.15s ease',
        }}>{co.name}</div>
        <div style={{ fontSize: '10px', color: '#3f3f46', letterSpacing: '0.02em' }}>
          {co.ticker} · {co.tags[0]}
        </div>
      </div>

      <div style={{
        color: active ? co.accent : '#3f3f46',
        opacity: active || hov ? 1 : 0,
        transform: active ? 'translateX(0)' : 'translateX(-3px)',
        transition: 'all 0.15s ease',
      }}>
        <IconChevron />
      </div>
    </button>
  );
}

// ── Landing tile ──────────────────────────────────────────────────────────────

function Tile({ co, onSelect }) {
  const [hov, setHov] = useState(false);

  return (
    <button
      onClick={() => onSelect(co.slug)}
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
      style={{
        width: '200px', padding: '28px 20px 24px',
        background: hov ? `rgba(${hexRgb(co.accent)},0.06)` : 'rgba(255,255,255,0.025)',
        border: `1px solid ${hov ? co.accent : '#27272a'}`,
        borderRadius: '18px', cursor: 'pointer', textAlign: 'center',
        transition: 'all 0.2s ease',
        transform: hov ? 'translateY(-6px)' : 'translateY(0)',
        boxShadow: hov ? `0 12px 40px rgba(${hexRgb(co.accent)},0.18)` : 'none',
      }}
    >
      {/* Logo avatar — centred */}
      <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '18px' }}>
        <Avatar co={co} size={58} shadow={hov} />
      </div>

      <div style={{ fontSize: '16px', fontWeight: '700', color: '#f4f4f5', letterSpacing: '-0.02em', marginBottom: '4px' }}>
        {co.name}
      </div>
      <div style={{ fontSize: '11px', color: '#52525b', letterSpacing: '0.02em', marginBottom: '14px' }}>
        {co.ticker}
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', justifyContent: 'center', marginBottom: '18px' }}>
        {co.tags.map(t => (
          <span key={t} style={{
            fontSize: '9px', fontWeight: '600', letterSpacing: '0.04em',
            color: hov ? co.accent : '#52525b',
            background: hov ? `rgba(${hexRgb(co.accent)},0.1)` : 'rgba(255,255,255,0.04)',
            padding: '2px 7px', borderRadius: '999px',
            transition: 'all 0.2s ease',
          }}>{t}</span>
        ))}
      </div>

      <div style={{
        fontSize: '11px', fontWeight: '600', letterSpacing: '0.04em',
        color: hov ? co.accent : '#3f3f46',
        transition: 'color 0.2s ease',
      }}>
        View Report →
      </div>
    </button>
  );
}

// ── Empty / landing state ─────────────────────────────────────────────────────

function EmptyState({ onSelect }) {
  return (
    <div style={{
      display: 'flex', flexDirection: 'column', alignItems: 'center',
      justifyContent: 'center', height: '100%', padding: '40px', gap: '52px',
      background: 'radial-gradient(ellipse 60% 50% at 50% 50%, rgba(66,133,244,0.04) 0%, transparent 70%)',
    }}>
      <div style={{ textAlign: 'center', maxWidth: '440px' }}>
        <div style={{
          display: 'inline-block', fontSize: '10px', fontWeight: '700',
          letterSpacing: '0.14em', color: '#3f3f46', textTransform: 'uppercase',
          marginBottom: '20px', padding: '4px 12px', borderRadius: '999px',
          border: '1px solid #27272a',
        }}>
          Partnership Intelligence Platform
        </div>
        <h1 style={{
          fontSize: '40px', fontWeight: '700', color: '#f4f4f5',
          letterSpacing: '-0.04em', lineHeight: '1.08', margin: '0 0 18px',
        }}>
          Select a company<br />to view its report
        </h1>
        <p style={{ fontSize: '15px', color: '#52525b', lineHeight: '1.65', margin: 0 }}>
          Eleven curated intelligence profiles ready for your review.<br />
          Search by name or click a card below.
        </p>
      </div>

      {/* 4 + 4 + 3 grid */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', alignItems: 'center' }}>
        <div style={{ display: 'flex', gap: '20px' }}>
          {COMPANIES.slice(0, 4).map(co => <Tile key={co.slug} co={co} onSelect={onSelect} />)}
        </div>
        <div style={{ display: 'flex', gap: '20px' }}>
          {COMPANIES.slice(4, 8).map(co => <Tile key={co.slug} co={co} onSelect={onSelect} />)}
        </div>
        <div style={{ display: 'flex', gap: '20px' }}>
          {COMPANIES.slice(8).map(co => <Tile key={co.slug} co={co} onSelect={onSelect} />)}
        </div>
      </div>
    </div>
  );
}

// ── Report viewer ─────────────────────────────────────────────────────────────

function ReportView({ co }) {
  const [dlHov, setDlHov] = useState(false);
  // Use Vite's BASE_URL so paths work on both localhost and GitHub Pages
  const pdfUrl = `${import.meta.env.BASE_URL}reports/${co.slug}.pdf`;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header bar */}
      <div style={{
        height: '60px', flexShrink: 0, padding: '0 28px',
        display: 'flex', alignItems: 'center', gap: '14px',
        background: '#0f0f11', borderBottom: '1px solid #1c1c1f',
      }}>
        <Avatar co={co} size={30} />

        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontSize: '13px', fontWeight: '600', color: '#e4e4e7', letterSpacing: '-0.01em' }}>
            {co.name}
            <span style={{ color: '#3f3f46', margin: '0 6px', fontWeight: '400' }}>·</span>
            <span style={{ color: '#71717a', fontWeight: '400' }}>Partnership Intelligence Report</span>
          </div>
          <div style={{ fontSize: '10px', color: '#3f3f46', marginTop: '2px', letterSpacing: '0.02em' }}>
            {co.parent} · {co.ticker} · Internal Use Only · May 2026
          </div>
        </div>

        <div style={{ display: 'flex', gap: '6px' }}>
          {co.tags.map(t => (
            <span key={t} style={{
              fontSize: '10px', fontWeight: '600', letterSpacing: '0.02em',
              color: co.accent,
              background: `rgba(${hexRgb(co.accent)},0.1)`,
              padding: '3px 9px', borderRadius: '999px',
              border: `1px solid rgba(${hexRgb(co.accent)},0.2)`,
            }}>{t}</span>
          ))}
        </div>

        <a
          href={pdfUrl}
          download={`${co.slug}-partnership-intelligence.pdf`}
          onMouseEnter={() => setDlHov(true)}
          onMouseLeave={() => setDlHov(false)}
          style={{
            display: 'flex', alignItems: 'center', gap: '7px',
            padding: '8px 16px',
            background: dlHov ? co.accent : `rgba(${hexRgb(co.accent)},0.12)`,
            color: dlHov ? '#fff' : co.accent,
            border: `1px solid rgba(${hexRgb(co.accent)},0.3)`,
            borderRadius: '8px', fontSize: '12px', fontWeight: '600',
            letterSpacing: '-0.01em', textDecoration: 'none', flexShrink: 0,
            transition: 'all 0.15s ease',
          }}
        >
          <IconDownload /> Download PDF
        </a>
      </div>

      {/* Thin company-coloured accent rule */}
      <div style={{
        height: '2px', flexShrink: 0,
        background: `linear-gradient(90deg, ${co.grad[0]}, ${co.grad[1]}, transparent)`,
      }} />

      {/* PDF iframe */}
      <div style={{ flex: 1, overflow: 'hidden', background: '#141416' }}>
        <iframe
          key={co.slug}
          src={pdfUrl}
          style={{ width: '100%', height: '100%', border: 'none', display: 'block' }}
          title={`${co.name} Partnership Intelligence Report`}
        />
      </div>
    </div>
  );
}

// ── Root ──────────────────────────────────────────────────────────────────────

export default function App() {
  const [query, setQuery] = useState('');
  const [selected, setSelected] = useState(null);

  const visible = filterCompanies(query);
  const co = COMPANIES.find(c => c.slug === selected) ?? null;

  const handleSelect = (slug) => { setSelected(slug); setQuery(''); };
  const handleKey = (e) => { if (e.key === 'Enter' && visible.length === 1) handleSelect(visible[0].slug); };

  return (
    <div style={{ display: 'flex', height: '100vh', background: '#09090b', overflow: 'hidden' }}>

      {/* ── Sidebar ─────────────────────────────────────────────────────────── */}
      <aside style={{
        width: '272px', flexShrink: 0,
        background: '#0f0f11', borderRight: '1px solid #1c1c1f',
        display: 'flex', flexDirection: 'column', height: '100vh',
      }}>
        {/* Brand — click to return home */}
        <div
          onClick={() => setSelected(null)}
          style={{ padding: '22px 18px 18px', cursor: 'pointer' }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '3px' }}>
            {/* App icon: retro CRT monitor */}
            <div style={{
              width: '30px', height: '30px', borderRadius: '8px',
              background: '#ffffff',
              border: '1px solid #e4e4e7',
              display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
            }}>
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                {/* Monitor bezel */}
                <rect x="1" y="1" width="18" height="12.5" rx="1.5" fill="#111111"/>
                {/* Screen glass */}
                <rect x="2.5" y="2.2" width="15" height="9.8" rx="0.8" fill="#0d0d0d"/>
                {/* Green phosphor glow — scanline text effect */}
                <rect x="4"   y="4"   width="5" height="1.1" rx="0.3" fill="#22c55e" opacity="0.9"/>
                <rect x="4"   y="6"   width="8" height="1.1" rx="0.3" fill="#22c55e" opacity="0.6"/>
                <rect x="4"   y="8"   width="6" height="1.1" rx="0.3" fill="#22c55e" opacity="0.6"/>
                {/* Blinking cursor block */}
                <rect x="10.2" y="4" width="1.2" height="1.1" rx="0.2" fill="#22c55e"/>
                {/* Neck */}
                <rect x="9" y="13.5" width="2" height="2.5" fill="#111111"/>
                {/* Base */}
                <rect x="5.5" y="16" width="9" height="1.6" rx="0.8" fill="#111111"/>
                {/* Screen glare highlight */}
                <rect x="3.5" y="3" width="3.5" height="1.2" rx="0.4" fill="white" opacity="0.07"/>
              </svg>
            </div>
            <div style={{ fontSize: '13px', fontWeight: '700', color: '#f4f4f5', letterSpacing: '-0.02em' }}>
              Partnership Intelligence
            </div>
          </div>
          <div style={{ fontSize: '10px', color: '#3f3f46', letterSpacing: '0.01em', paddingLeft: '40px', fontFamily: 'monospace' }}>
            partnership-intelligence-analyzer
          </div>
        </div>

        <div style={{ height: '1px', background: '#1c1c1f', margin: '0 18px 14px' }} />

        {/* Search */}
        <div style={{ padding: '0 12px 10px' }}>
          <div style={{
            display: 'flex', alignItems: 'center', gap: '8px',
            background: '#18181b', border: '1px solid #27272a',
            borderRadius: '9px', padding: '9px 12px',
          }}>
            <IconSearch />
            <input
              value={query}
              onChange={e => setQuery(e.target.value)}
              onKeyDown={handleKey}
              placeholder="Search companies…"
              style={{
                flex: 1, background: 'none', border: 'none', outline: 'none',
                fontSize: '13px', color: '#f4f4f5', caretColor: '#4285f4',
              }}
              autoComplete="off" spellCheck={false}
            />
            {query && (
              <button onClick={() => setQuery('')} style={{
                background: 'none', border: 'none', cursor: 'pointer',
                color: '#52525b', fontSize: '15px', lineHeight: 1, padding: '0 2px',
                display: 'flex', alignItems: 'center',
              }}>×</button>
            )}
          </div>
        </div>

        {/* List label */}
        <div style={{ padding: '4px 18px 8px', fontSize: '9px', fontWeight: '700', color: '#27272a', letterSpacing: '0.1em', textTransform: 'uppercase' }}>
          Companies · {visible.length}/{COMPANIES.length}
        </div>

        {/* Company list */}
        <div style={{ flex: 1, padding: '0 6px', overflowY: 'auto' }}>
          {visible.length === 0
            ? <div style={{ padding: '24px 12px', fontSize: '12px', color: '#3f3f46', textAlign: 'center' }}>No matches found</div>
            : visible.map(c => (
                <CompanyCard key={c.slug} co={c} selected={selected} onSelect={() => handleSelect(c.slug)} />
              ))
          }
        </div>

        {/* Footer */}
        <div style={{ padding: '14px 18px', borderTop: '1px solid #1c1c1f' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#22c55e', boxShadow: '0 0 6px #22c55e' }} />
            <span style={{ fontSize: '10px', color: '#3f3f46', fontWeight: '500', letterSpacing: '0.03em' }}>
              Demo · 11 reports available
            </span>
          </div>
        </div>
      </aside>

      {/* ── Main panel ──────────────────────────────────────────────────────── */}
      <main style={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        {co ? <ReportView co={co} /> : <EmptyState onSelect={handleSelect} />}
      </main>
    </div>
  );
}
