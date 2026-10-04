export type Language = 'en' | 'hi' | 'mr';

export const t = (key: string, lang?: Language): string => {
  return key;
};
