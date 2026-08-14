// Mock data for the Sentinel AI dashboard.
// Shapes here are the contract the real API should eventually satisfy —
// see src/services/api.js for where these calls will be swapped in.

export const securityOverview = {
  status: 'protected', // 'protected' | 'at_risk' | 'critical'
  statusLabel: 'System Protected',
  riskScore: 24, // 0-100, higher = riskier
  riskLevel: 'LOW', // LOW | MEDIUM | HIGH | CRITICAL — sent explicitly by the backend
  riskTrend: -6, // change vs. last 7 days
  threatCount: 3,
  eventCount24h: 128,
  criticalAlerts: 1,
  lastScan: '12 minutes ago',
};

export const recentThreats = [
  {
    id: 1,
    severity: 'critical',
    title: 'Suspicious PowerShell Activity',
    description: 'Encoded command executed via PowerShell, differing from normal system behavior.',
    process: 'powershell.exe',
    timestamp: '10:42 AM',
  },
  {
    id: 2,
    severity: 'high',
    title: 'Unusual Outbound Connection',
    description: 'Repeated connection attempts to an unrecognized external IP range.',
    process: 'svchost.exe',
    timestamp: '9:15 AM',
  },
  {
    id: 3,
    severity: 'medium',
    title: 'Modified Registry Autorun Key',
    description: 'A startup entry was added outside of any known installer.',
    process: 'regedit.exe',
    timestamp: 'Yesterday, 8:03 PM',
  },
  {
    id: 4,
    severity: 'low',
    title: 'Blocked Macro in Downloaded Document',
    description: 'Office macro execution was blocked on a file from an email attachment.',
    process: 'winword.exe',
    timestamp: 'Yesterday, 3:47 PM',
  },
];

// Last 7 days of activity, used by ActivityChart
export const activityData = [
  { day: 'Mon', detected: 14, blocked: 12 },
  { day: 'Tue', detected: 9, blocked: 9 },
  { day: 'Wed', detected: 22, blocked: 19 },
  { day: 'Thu', detected: 17, blocked: 17 },
  { day: 'Fri', detected: 31, blocked: 27 },
  { day: 'Sat', detected: 11, blocked: 11 },
  { day: 'Sun', detected: 8, blocked: 8 },
];

export const systemStatus = [
  { id: 'firewall', name: 'Firewall', detail: 'Inbound & outbound rules active', status: 'active' },
  { id: 'defender', name: 'Real-time Protection', detail: 'Windows Defender engine running', status: 'active' },
  { id: 'updates', name: 'Security Updates', detail: '2 optional updates pending', status: 'warning' },
  { id: 'vpn', name: 'Network Encryption', detail: 'VPN not connected', status: 'inactive' },
];

export const notifications = {
  unreadCount: 4,
};

// --- Security Events log (full list for the Events page) ---
// Same shape as recentThreats, so it can reuse AIExplanation with zero changes.
export const securityEvents = [
  { id: 201, severity: 'critical', title: 'Suspicious PowerShell Activity', description: 'Encoded command executed via PowerShell, differing from normal system behavior.', process: 'powershell.exe', category: 'process', device: 'DESKTOP-J4KQ2', timestamp: '10:42 AM' },
  { id: 202, severity: 'medium',   title: 'New Process',                   description: 'An unfamiliar process was launched by an unrecognized parent.', process: 'unknown.exe', category: 'process', device: 'DESKTOP-J4KQ2', timestamp: '10:35 AM' },
  { id: 203, severity: 'high',     title: 'Network Connection',            description: 'Repeated connection attempts to an unrecognized external IP range.', process: 'svchost.exe', category: 'network', device: 'SRV-WEB03', timestamp: '10:28 AM' },
  { id: 204, severity: 'low',      title: 'File Modification',             description: 'A document file was modified by its owning application.', process: 'winword.exe', category: 'files', device: 'LAPTOP-R7T1', timestamp: '10:20 AM' },
  { id: 205, severity: 'low',      title: 'Login Event',                   description: 'Successful sign-in from a recognized device.', process: 'lsass.exe', category: 'authentication', device: 'acct: j.rivera', timestamp: '10:12 AM' },
  { id: 206, severity: 'medium',   title: 'Registry Change',               description: 'A startup entry was added outside of any known installer.', process: 'regedit.exe', category: 'system', device: 'DESKTOP-M2QX', timestamp: '9:58 AM' },
  { id: 207, severity: 'high',     title: 'Failed Login Attempt',          description: 'Multiple failed sign-in attempts in a short window.', process: 'lsass.exe', category: 'authentication', device: 'acct: t.okafor', timestamp: '9:41 AM' },
  { id: 208, severity: 'low',      title: 'USB Device Connected',          description: 'A removable storage device was connected.', process: 'explorer.exe', category: 'system', device: 'LAPTOP-C9F4', timestamp: '9:15 AM' },
];

// --- Chart 2: Threat distribution ---
export const riskDistribution = [
  { name: 'Low', value: 52, color: '#6BCB8F' },
  { name: 'Medium', value: 28, color: '#F0CC53' },
  { name: 'High', value: 15, color: '#FF9451' },
  { name: 'Critical', value: 5, color: '#FF5C7A' },
];

// --- Chart 3: Activity by category ---
export const categoryActivity = [
  { category: 'Processes', count: 48 },
  { category: 'Network', count: 35 },
  { category: 'Files', count: 27 },
  { category: 'Authentication', count: 19 },
  { category: 'System', count: 12 },
];

// Canned AI analysis, keyed by id — covers both recentThreats and securityEvents.
// Matches the shape GET /api/threats/:id/analysis is expected to return.
const analysisById = {
  1: {
    summary: "PowerShell executed an encoded command that differs from this system's normal behavior, launched from a non-standard process path.",
    whySuspicious: ['Unusual execution pattern for this user session', 'Command was base64-encoded to obscure its contents', 'Activity occurred outside normal usage hours'],
    recommendation: 'Review the PowerShell process and terminate it if you do not recognize the activity. Consider isolating this device from the network until reviewed.',
  },
  2: {
    summary: 'A background system process attempted repeated outbound connections to an IP range not previously seen on this network.',
    whySuspicious: ['Unrecognized destination IP range', 'Unusually high connection frequency', 'No matching entry in the allowed connections list'],
    recommendation: 'Block the destination IP range at the firewall and monitor for further attempts from the same process.',
  },
  3: {
    summary: 'A new entry was added to the Windows startup registry key outside of any tracked software installation.',
    whySuspicious: ['No corresponding installer was recorded', 'Autorun entries are a common persistence technique'],
    recommendation: 'Verify the referenced file is legitimate. Remove the registry entry if it cannot be attributed to trusted software.',
  },
  4: {
    summary: 'An Office macro embedded in an email attachment attempted to run and was blocked automatically before execution.',
    whySuspicious: ['Macro originated from an external email attachment', 'Macro execution is disabled by policy for untrusted documents'],
    recommendation: 'No action required — the macro was blocked automatically. Confirm the sender is expected before opening similar attachments in future.',
  },
  201: {
    summary: "PowerShell executed an encoded command that differs from this device's normal behavior, launched by an unexpected parent process.",
    whySuspicious: ['Unusual execution pattern — base64-encoded arguments rarely used on this device', 'Unexpected parent process', 'Activity occurred outside normal usage hours'],
    recommendation: 'Review the process and terminate it if you do not recognize the activity.',
  },
  203: {
    summary: 'A process opened repeated outbound connections to an external IP range not seen from this device before.',
    whySuspicious: ['Destination has no prior connection history from this network', 'Connection attempts exceed this device\u2019s normal baseline'],
    recommendation: 'Investigate the destination and block the connection if it cannot be attributed to known software.',
  },
  207: {
    summary: 'Multiple sign-in attempts failed for this account in a short window.',
    whySuspicious: ['Attempt volume exceeds this account\u2019s typical pattern'],
    recommendation: 'Confirm the account owner isn\u2019t simply locked out; consider a temporary lockout otherwise.',
  },
};

// Fallback for any threat/event without a specific canned analysis above,
// so this never crashes on unexpected/future mock items.
function genericAnalysis(item) {
  return {
    summary: item.description ?? `${item.title} was detected and compared against this device's activity baseline.`,
    whySuspicious: item.severity === 'low'
      ? ['Pattern is consistent with expected behavior for this device']
      : ['Flagged by automated detection rules', 'Does not match known-safe activity for this system'],
    recommendation: item.severity === 'low'
      ? 'No action required — logged for visibility.'
      : 'Review this activity and confirm whether it was expected before dismissing.',
  };
}

// Single source of truth — Dashboard's ThreatCard AND Events.jsx both call this.
export function getThreatAnalysis(item) {
  return analysisById[item.id] ?? genericAnalysis(item);
}