import { type Page } from './pages';

export const artLevels = ['easy', 'medium', 'detailed'] as const;
export type ArtLevel = typeof artLevels[number];
export const levelNames = {
  bg: { easy: 'Лесно', medium: 'Средно', detailed: 'Детайлно' },
  en: { easy: 'Easy', medium: 'Medium', detailed: 'Detailed' },
};
export const reviewSubjects = [
  { id: 'cat', bg: 'Коте в градината', en: 'Garden kitten' },
  { id: 'car', bg: 'Семейна кола', en: 'Family hatchback' },
  { id: 'mountain', bg: 'Планинско езеро', en: 'Alpine lake' },
];
// Geometry changes must never be applied to old freehand coordinates. Preserve
// v1 saves verbatim; each v2 level has its own stable document identity.
export const reviewPages: Page[] = reviewSubjects.flatMap(subject => artLevels.map(level => ({
  id: `${subject.id}@v2:${level}`,
  category: 'art-review',
  title: {
    bg: `${subject.bg} · ${levelNames.bg[level]}`,
    en: `${subject.en} · ${levelNames.en[level]}`,
  },
  difficulty: level === 'detailed' ? 'advanced' : level,
  asset: `/illustrations/v2/${level}/${subject.id}.svg`,
  artVersion: 2,
})));
