// Engagement Letter Template for Ruh AI
// This is the reference template. When generating a letter, copy this file,
// fill in the CONFIG section with the client's information, and run with Node.js.
//
// Usage: node generate-letter.js
// Output: engagement-letter.docx

const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, HeadingLevel,
  LevelFormat
} = require("docx");

// ============================================================================
// CONFIG — Fill in these values for each engagement
// ============================================================================

const CONFIG = {
  // Client info
  clientName: "David Gallo",               // Primary contact name
  companyName: "[Company Name]",            // Client company
  address: "[Address]",                     // Street address
  cityStateZip: "[City, State ZIP]",        // City, State ZIP

  // Participants — array of names
  participants: [
    "David Gallo",
    "David [Last Name]",
    "Ryan [Last Name]",
  ],

  // Engagement details
  engagementName: "AI Enablement Engagement",
  engagementDescription: "designed to get your team fully operational with Claude AI across your real workflows",

  // What participants walk away with — array of { bold, rest } objects
  outcomes: [
    { bold: "A fully configured Claude environment", rest: " connected to their actual business tools (email, calendar, documents, and other daily systems)" },
    { bold: "Custom-built Skills", rest: " tailored to their specific role and responsibilities" },
    { bold: "Working, repeatable workflows", rest: " they can use on day one without further assistance" },
    { bold: "The knowledge and confidence", rest: " to identify new use cases and build additional workflows on their own" },
    { bold: "Written documentation", rest: " of everything built during the engagement for reference and team sharing" },
  ],

  // The outcome summary line (bold portion)
  outcomeSummary: "actively using AI to do their jobs better",

  // How We Get There — phase descriptions
  phases: {
    discovery: "We start by understanding your current workflows, the tools your team uses daily, and where the biggest opportunities are to reduce workload. This shapes everything that follows.",
    plan: "Based on what we learn, I\u2019ll put together a targeted plan covering which workflows we\u2019ll build, which integrations we\u2019ll connect, and what each participant\u2019s setup will look like.",
    build: "This is the core of the engagement. We work together in hands-on sessions where participants build their workflows on their actual work\u2014not hypothetical exercises. We configure Claude Desktop and Claude Code, build custom Skills, connect integrations, set up the scheduler, and get everything running. I work alongside each participant until their workflows are functional and they\u2019re comfortable operating independently.",
    verify: "We wrap up by reviewing everything that was built, confirming each participant is self-sufficient, and documenting the full setup for future reference and team sharing.",
  },

  // Pricing
  price: 5000,                              // Flat fee in dollars
  additionalParticipantFee: 1500,           // Per additional person
  maxGroupSize: 5,                          // Maximum participants
  paymentSplit: [50, 50],                   // Percentage split [signing, completion]
  paymentMethods: "wire transfer, ACH, or check",

  // Logistics
  deliveryMethod: "video conference unless otherwise arranged",
  completionWindow: "4 weeks of kickoff",
  completionDeadline: "60 days of signing",
  letterValidDays: 30,
  cancellationNoticeDays: 7,

  // Prerequisites — array of strings
  prerequisites: [
    "An active Claude Pro ($20/month) or Claude Team subscription",
    "Claude Desktop application installed on their primary workstation",
    "Access to their standard business tools for integration setup",
  ],

  // Scope exclusions — array of strings
  exclusions: [
    "Custom AI agent development or deployment",
    "Ongoing support or retainer services",
    "Software licensing fees",
    "Enterprise AI strategy consulting",
  ],

  // Follow-up teaser (mention of future agent work, or null to omit)
  followUpTeaser: "As discussed, once your team is comfortable with Claude\u2019s capabilities, we\u2019d welcome a follow-up conversation with you and Brian to explore building a dedicated AI agent for specific functions such as recruiting or estimating.",

  // Guarantee
  includeGuarantee: true,
  refundRequestDays: 14,                    // Days after final session to request refund

  // Agent build credit
  includeAgentCredit: true,
  agentCreditMonths: 6,                     // Months window for credit

  // Sender
  senderName: "Jesse Anglen",
  senderTitle: "Co-Founder & CEO, Ruh AI",
  senderContact: "[email] | [phone]",

  // Output
  outputPath: "engagement-letter.docx",
};

// ============================================================================
// TEMPLATE — Do not modify below unless changing the letter structure
// ============================================================================

const COLORS = { primary: "1B3A5C", gray: "666666", white: "FFFFFF", lightGray: "F2F2F2" };
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

const today = new Date();
const dateStr = today.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });

const fmt = (amount) => `$${amount.toLocaleString("en-US", { minimumFractionDigits: 0 })}`;
const deposit = Math.round(CONFIG.price * CONFIG.paymentSplit[0] / 100);
const balance = CONFIG.price - deposit;

// Helper to create bullet items
function bullet(ref, text, spacing = 60) {
  return new Paragraph({
    numbering: { reference: ref, level: 0 },
    spacing: { after: spacing },
    children: Array.isArray(text) ? text : [new TextRun(text)],
  });
}

// Helper for phase blocks
function phase(title, description) {
  return [
    new Paragraph({
      spacing: { before: 200, after: 80 },
      children: [new TextRun({ text: title, bold: true, color: COLORS.primary })],
    }),
    new Paragraph({
      spacing: { after: 120 },
      children: [new TextRun(description)],
    }),
  ];
}

// Build the children array
const children = [];

// --- HEADER ---
children.push(
  new Paragraph({ spacing: { after: 0 }, children: [new TextRun({ text: "RUH AI", size: 36, bold: true, color: COLORS.primary })] }),
  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "Autonomous AI Solutions", size: 20, color: COLORS.gray, italics: true })] }),
  new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: COLORS.primary, space: 1 } }, spacing: { after: 400 }, children: [] }),
);

// --- DATE & ADDRESSEE ---
children.push(
  new Paragraph({ spacing: { after: 200 }, children: [new TextRun(dateStr)] }),
  new Paragraph({ spacing: { after: 0 }, children: [new TextRun(CONFIG.clientName)] }),
  new Paragraph({ spacing: { after: 0 }, children: [new TextRun(CONFIG.companyName)] }),
  new Paragraph({ spacing: { after: 0 }, children: [new TextRun(CONFIG.address)] }),
  new Paragraph({ spacing: { after: 300 }, children: [new TextRun(CONFIG.cityStateZip)] }),
);

// --- OPENING ---
children.push(
  new Paragraph({ spacing: { after: 200 }, children: [new TextRun(`Dear ${CONFIG.clientName.split(" ")[0]},`)] }),
  new Paragraph({
    spacing: { after: 200 },
    children: [
      new TextRun(`Thank you for the productive conversation about how AI can support your team\u2019s day-to-day operations. Per your request, this letter outlines the terms and scope of an ${CONFIG.engagementName} ${CONFIG.engagementDescription}.`),
    ],
  }),
);

// --- SECTION 1: THE OUTCOME ---
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("1. The Outcome")] }));
children.push(new Paragraph({
  spacing: { after: 200 },
  children: [new TextRun("At the conclusion of this engagement, each participant will be independently capable of using Claude AI to meaningfully reduce their daily workload. Specifically, each participant will walk away with:")],
}));

CONFIG.outcomes.forEach((o, i) => {
  children.push(bullet("bullets", [
    new TextRun({ text: o.bold, bold: true }),
    new TextRun(o.rest),
  ], i === CONFIG.outcomes.length - 1 ? 200 : 60));
});

children.push(new Paragraph({
  spacing: { after: 200 },
  children: [
    new TextRun("The goal is not just training\u2014it\u2019s getting your people to a point where they are "),
    new TextRun({ text: CONFIG.outcomeSummary, bold: true }),
    new TextRun(", with real workflows running on real work, before we\u2019re done."),
  ],
}));

// --- SECTION 2: HOW WE GET THERE ---
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("2. How We Get There")] }));
children.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun("The engagement follows a simple progression:")] }));
children.push(...phase("Discovery", CONFIG.phases.discovery));
children.push(...phase("Plan", CONFIG.phases.plan));
children.push(...phase("Build", CONFIG.phases.build));
children.push(...phase("Verify & Handoff", CONFIG.phases.verify));

// --- SECTION 3: PARTICIPANTS ---
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("3. Participants")] }));
children.push(new Paragraph({
  spacing: { after: 200 },
  children: [
    new TextRun("This engagement covers up to "),
    new TextRun({ text: `${CONFIG.participants.length} (${["zero","one","two","three","four","five"][CONFIG.participants.length]})`, bold: true }),
    new TextRun(" participants:"),
  ],
}));

CONFIG.participants.forEach((name, i) => {
  children.push(new Paragraph({
    numbering: { reference: "numbers", level: 0 },
    spacing: { after: i === CONFIG.participants.length - 1 ? 200 : 60 },
    children: [new TextRun(name)],
  }));
});

children.push(new Paragraph({
  spacing: { after: 200 },
  children: [new TextRun(`Additional participants may be added at ${fmt(CONFIG.additionalParticipantFee)} per person, with a maximum group size of ${CONFIG.maxGroupSize}.`)],
}));

// --- SECTION 4: INVESTMENT ---
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("4. Investment")] }));

children.push(new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [6000, 3360],
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders, width: { size: 6000, type: WidthType.DXA }, margins: cellMargins,
          shading: { fill: COLORS.primary, type: ShadingType.CLEAR },
          children: [new Paragraph({ children: [new TextRun({ text: "Engagement", bold: true, color: COLORS.white })] })],
        }),
        new TableCell({
          borders, width: { size: 3360, type: WidthType.DXA }, margins: cellMargins,
          shading: { fill: COLORS.primary, type: ShadingType.CLEAR },
          children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Flat Fee", bold: true, color: COLORS.white })] })],
        }),
      ],
    }),
    new TableRow({
      children: [
        new TableCell({
          borders, width: { size: 6000, type: WidthType.DXA }, margins: cellMargins,
          children: [
            new Paragraph({ children: [new TextRun(CONFIG.engagementName)] }),
            new Paragraph({ spacing: { before: 40 }, children: [new TextRun({ text: `Discovery through verified handoff for up to ${CONFIG.participants.length} participants`, italics: true, color: COLORS.gray, size: 20 })] }),
          ],
        }),
        new TableCell({
          borders, width: { size: 3360, type: WidthType.DXA }, margins: cellMargins,
          verticalAlign: "center",
          children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: fmt(CONFIG.price), bold: true, size: 28 })] })],
        }),
      ],
    }),
  ],
}));

children.push(new Paragraph({ spacing: { before: 300, after: 100 }, children: [new TextRun({ text: "Payment Terms:", bold: true })] }));
children.push(bullet("bullets", `${CONFIG.paymentSplit[0]}% (${fmt(deposit)}) due upon signing to reserve engagement dates`));
children.push(bullet("bullets", `${CONFIG.paymentSplit[1]}% (${fmt(balance)}) due upon completion`));
children.push(bullet("bullets", `Payment accepted via ${CONFIG.paymentMethods}`, 200));

// --- SECTION 5: LOGISTICS ---
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("5. Logistics")] }));
children.push(bullet("bullets", `Sessions are conducted via ${CONFIG.deliveryMethod}`));
children.push(bullet("bullets", "Scheduling is coordinated mutually based on participant availability"));
children.push(bullet("bullets", `The engagement is expected to be completed within ${CONFIG.completionWindow}`, 200));

// --- SECTION 6: PREREQUISITES ---
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("6. Prerequisites")] }));
children.push(new Paragraph({ spacing: { after: 80 }, children: [new TextRun("Each participant should have the following ready before the first working session:")] }));
CONFIG.prerequisites.forEach((p, i) => {
  children.push(bullet("bullets", p, i === CONFIG.prerequisites.length - 1 ? 200 : 60));
});

// --- SECTION 7: SCOPE & BOUNDARIES ---
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("7. Scope & Boundaries")] }));
children.push(new Paragraph({ spacing: { after: 80 }, children: [new TextRun("This engagement is focused on enabling your team to use Claude AI effectively. The following are available as separate engagements:")] }));
CONFIG.exclusions.forEach((e, i) => {
  children.push(bullet("bullets", e, i === CONFIG.exclusions.length - 1 ? 200 : 60));
});

if (CONFIG.followUpTeaser) {
  children.push(new Paragraph({ spacing: { after: 200 }, children: [new TextRun(CONFIG.followUpTeaser)] }));
}

// --- SECTION 8: TERM & CANCELLATION ---
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("8. Term & Cancellation")] }));
children.push(bullet("bullets", `This engagement letter is valid for ${CONFIG.letterValidDays} days from the date above`));
children.push(bullet("bullets", `Either party may cancel with ${CONFIG.cancellationNoticeDays} days written notice`));
children.push(bullet("bullets", "If cancelled after discovery, the initial deposit is non-refundable"));
children.push(bullet("bullets", `The engagement must be completed within ${CONFIG.completionDeadline}`, 300));

// --- SECTION 9: SATISFACTION GUARANTEE ---
if (CONFIG.includeGuarantee) {
  children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("9. Satisfaction Guarantee")] }));
  children.push(new Paragraph({
    spacing: { after: 200 },
    children: [new TextRun("We stand behind the value of this engagement. If, upon completion, you feel that your team did not gain meaningful, practical capability from the experience, we will refund your investment in full\u2014no questions asked.")],
  }));
  children.push(new Paragraph({
    spacing: { after: 200 },
    children: [new TextRun("The only requirement is that all designated participants attend and actively participate in the scheduled sessions. This guarantee reflects our confidence that if your team shows up and engages, they will walk away with workflows that make a real difference in their day-to-day work.")],
  }));
  children.push(new Paragraph({
    spacing: { after: 200 },
    children: [new TextRun(`A refund request must be submitted in writing within ${CONFIG.refundRequestDays} days of the final session.`)],
  }));
}

// --- SECTION 10: AGENT BUILD CREDIT ---
if (CONFIG.includeAgentCredit) {
  const sectionNum = CONFIG.includeGuarantee ? 10 : 9;
  children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(`${sectionNum}. Agent Build Credit`)] }));
  children.push(new Paragraph({
    spacing: { after: 200 },
    children: [new TextRun(`If, within ${CONFIG.agentCreditMonths} months of completing this engagement, you choose to engage Ruh AI to build a dedicated AI agent for your organization, the full ${fmt(CONFIG.price)} paid for this enablement engagement will be credited toward the agent build. In effect, the coaching is free when you move forward with us on an agent.`)],
  }));
  children.push(new Paragraph({
    spacing: { after: 200 },
    children: [new TextRun(`This credit applies to any Ruh AI agent engagement signed within the ${CONFIG.agentCreditMonths}-month window and cannot be combined with any other discounts or promotions.`)],
  }));
}

// --- DIVIDER ---
children.push(new Paragraph({
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: COLORS.primary, space: 1 } },
  spacing: { after: 300 },
  children: [],
}));

// --- CLOSING ---
children.push(new Paragraph({
  spacing: { after: 200 },
  children: [new TextRun("If this works for you, sign below and return this letter along with the initial deposit. I look forward to working with your team.")],
}));
children.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun("Warm regards,")] }));
children.push(new Paragraph({ spacing: { after: 0 }, children: [] }));
children.push(new Paragraph({ spacing: { after: 0 }, children: [] }));
children.push(new Paragraph({ spacing: { after: 0 }, children: [new TextRun({ text: CONFIG.senderName, bold: true })] }));
children.push(new Paragraph({ spacing: { after: 0 }, children: [new TextRun(CONFIG.senderTitle)] }));
children.push(new Paragraph({ spacing: { after: 400 }, children: [new TextRun({ text: CONFIG.senderContact, color: COLORS.gray, size: 20 })] }));

// --- SIGNATURE BLOCK ---
children.push(new Paragraph({ spacing: { before: 200, after: 200 }, children: [new TextRun({ text: "ACCEPTED AND AGREED:", bold: true, color: COLORS.primary })] }));
children.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun("Signature: ___________________________________________")] }));
children.push(new Paragraph({ spacing: { after: 200 }, children: [] }));
children.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun("Printed Name: ________________________________________")] }));
children.push(new Paragraph({ spacing: { after: 200 }, children: [] }));
children.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun("Title: ________________________________________________")] }));
children.push(new Paragraph({ spacing: { after: 200 }, children: [] }));
children.push(new Paragraph({ spacing: { after: 60 }, children: [new TextRun("Date: ________________________________________________")] }));

// ============================================================================
// BUILD DOCUMENT
// ============================================================================

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial", color: COLORS.primary },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 },
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: COLORS.primary },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 },
      },
    ],
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }],
      },
      {
        reference: "numbers",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }],
      },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    children,
  }],
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(CONFIG.outputPath, buffer);
  console.log(`Generated: ${CONFIG.outputPath}`);
});
