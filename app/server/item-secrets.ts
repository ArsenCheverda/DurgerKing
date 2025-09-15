export const ITEM_SECRETS: Record<string, string> = {
    'ice_cream': 'FROZEN2025',
    'cookie': 'SWEET2025',
    'hamburger': 'BURGER2025'
};

export function getSecretForItem(itemId: string): string | undefined {
    return ITEM_SECRETS[itemId];
}