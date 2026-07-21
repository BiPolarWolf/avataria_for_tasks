// ============================================================================
//  ТЕМЫ — единственная точка входа (прототип, путь А)
// ============================================================================
//  Тема = несколько СМЫСЛОВЫХ цветов с человеческими именами.
//  Оттенки (hover / active / приподнятая поверхность / тень и т.п.) выводятся
//  автоматически в tokens.css через color-mix — здесь их писать НЕ нужно.
//
//  Добавить новую тему: скопируй объект ниже, поменяй 6 цветов, добавь в THEMES.
//  Больше ничего трогать не нужно — ни main.css, ни компоненты, ни превью.
// ============================================================================

export interface ThemeColors {
  /** Фон страницы */
  background: string
  /** Поверхность карточек и панелей */
  surface: string
  /** Основной текст */
  text: string
  /** Приглушённый / второстепенный текст */
  muted: string
  /** Акцент: бренд, активные элементы, ссылки */
  accent: string
  /** Границы и разделители */
  border: string
  /** Текст поверх акцентной заливки. По умолчанию белый. */
  accentText?: string
}

export interface Theme {
  /** Уникальный id (сохраняется в localStorage) */
  id: string
  /** Название для UI настроек */
  label: string
  /** Смысловые цвета темы */
  colors: ThemeColors
  /** Основной шрифт интерфейса (опционально) */
  font?: string
}

/** Хелпер-обёртка: даёт автокомплит и проверку типов при описании темы. */
export function defineTheme(theme: Theme): Theme {
  return theme
}

// --- Тема по умолчанию (бывший «Пергамент»). Теперь живёт ЗДЕСЬ, а не в main.css.
const parchment = defineTheme({
  id: 'parchment',
  label: 'Пергамент',
  colors: {
    background: '#e9dac9',
    surface: '#f4e7d7',
    text: '#2b2119',
    muted: '#8a7867',
    accent: '#997577',
    border: '#d9c4ac',
  },
  // Книжная антиква: читаемо и в духе бумаги/пергамента. Системные шрифты — без CDN.
  font: "Georgia, 'Palatino Linotype', 'Book Antiqua', 'Iowan Old Style', serif",
})

// --- Тёмная тема. Обрати внимание: НИКАКОЙ инверсии шкал, просто цвета ролей.
const midnight = defineTheme({
  id: 'midnight',
  label: 'Полночь',
  colors: {
    background: '#172430',
    surface: '#1e2024',
    text: '#f1f2f3',
    muted: '#898989ff',
    accent: '#60b3eaff',
    border: '#343841',
  },
  font: "'SanFrancisco', system-ui, sans-serif",
})

const cozyPixelRpg = defineTheme({
  id: 'cozy-pixel-rpg',
  label: 'Cozy Pixel RPG',
  colors: {
    background: '#d6b78d',
    surface: '#f8dfbf',
    text: '#2f2419',
    muted: '#6b513b',
    accent: '#6f9f5f',
    border: '#7b4f2f',
    accentText: '#fffbea',
  },
  font: "'PixeloidSans', 'Pixel', sans-serif",
})

const forestGuild = defineTheme({
  id: 'forest-guild',
  label: 'Forest Guild',
  colors: {
    background: '#b8a170',
    surface: '#e8d8b6',
    text: '#26301f',
    muted: '#63704c',
    accent: '#8c5f3d',
    border: '#53623a',
    accentText: '#fff4dc',
  },
  font: "Georgia, 'Palatino Linotype', 'Book Antiqua', 'Iowan Old Style', serif",
})

export const THEMES: Theme[] = [parchment, midnight, cozyPixelRpg, forestGuild]

export const DEFAULT_THEME_ID = parchment.id

export function getTheme(id: string): Theme {
  return THEMES.find((t) => t.id === id) ?? parchment
}

/**
 * Разворачивает смысловые цвета темы в CSS-переменные для :root.
 * Пишем ТОЛЬКО базовые токены — производные оттенки считает tokens.css.
 * Набор ключей одинаков у всех тем, поэтому при переключении ничего
 * «сбрасывать» не нужно (в отличие от старого ALL_THEME_KEYS).
 */
export function themeToVars(theme: Theme): Record<string, string> {
  const c = theme.colors
  return {
    '--background': c.background,
    '--surface': c.surface,
    '--text': c.text,
    '--muted': c.muted,
    '--accent': c.accent,
    '--accent-text': c.accentText ?? '#ffffff',
    '--border': c.border,
    '--font-body': theme.font ?? "'PixeloidSans', sans-serif",
  }
}
