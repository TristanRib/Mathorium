export class MathHelper {
    static generateRange(n: number): number[] {
        return Array.from({length: n}, (_, i) => i + 1);
    }

    static mean(arr: number[]) {
        return arr.reduce((acc, val) => acc + val, 0) / arr.length;
    }

    static median(arr: number[]) {
        const sorted = [...arr].sort((a, b) => a - b);
        const middle = Math.floor(sorted.length / 2);
        return sorted.length % 2 === 0 ? (sorted[middle - 1] + sorted[middle]) / 2 : sorted[middle];
    }

    static calculateStats(arr: number[]) {
        return {
            mean: MathHelper.mean(arr),
            median: MathHelper.median(arr),
            min: Math.min(...arr),
            max: Math.max(...arr),
        }
    };
}