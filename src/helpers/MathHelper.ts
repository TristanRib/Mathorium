export class MathHelper {
    static generateRange(n: number): number[] {
        return Array.from({length: n}, (_, i) => i + 1);
    }
}