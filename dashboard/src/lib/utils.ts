import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { cubicOut } from "svelte/easing";
import type { TransitionConfig } from "svelte/transition";

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

type FlyAndScaleParams = {
	y?: number;
	x?: number;
	start?: number;
	duration?: number;
};

export const flyAndScale = (
	node: Element,
	params: FlyAndScaleParams = { y: -8, x: 0, start: 0.95, duration: 150 }
): TransitionConfig => {
	const style = getComputedStyle(node);
	const transform = style.transform === "none" ? "" : style.transform;

	const scaleConversion = (
		valueA: number,
		scaleA: [number, number],
		scaleB: [number, number]
	) => {
		const [minA, maxA] = scaleA;
		const [minB, maxB] = scaleB;

		const percentage = (valueA - minA) / (maxA - minA);
		const valueB = percentage * (maxB - minB) + minB;

		return valueB;
	};

	const styleToString = (
		style: Record<string, number | string | undefined>
	): string => {
		return Object.keys(style).reduce((str, key) => {
			if (style[key] === undefined) return str;
			return str + `${key}:${style[key]};`;
		}, "");
	};

	return {
		duration: params.duration ?? 200,
		delay: 0,
		css: (t) => {
			const y = scaleConversion(t, [0, 1], [params.y ?? 5, 0]);
			const x = scaleConversion(t, [0, 1], [params.x ?? 0, 0]);
			const scale = scaleConversion(t, [0, 1], [params.start ?? 0.95, 1]);

			return styleToString({
				transform: `${transform} translate3d(${x}px, ${y}px, 0) scale(${scale})`,
				opacity: t
			});
		},
		easing: cubicOut
	};
};

import { tick } from 'svelte';

export async function closeAndFocusTrigger(triggerId: string) {
  tick().then(() => {
    document.getElementById(triggerId)?.focus();
  });
}

export const availableModelProviders = ['Anthropic', 'Azure', 'Cohere', 'Google', 'Groq', 'Hugging Face', 'Mistral', 'OpenAI'];

export const commonModels: Record<string, string[]> = {
  'OpenAI': [
    'gpt-5', 'gpt-5.1', 'gpt-5-mini', 'gpt-5-nano', 
    'gpt-4o', 'gpt-4o-mini', 
    'o1', 'o1-mini', 'o3', 'o3-mini'
  ],
  'Anthropic': [
    'claude-sonnet-4-5', 'claude-haiku-4-5', 'claude-opus-4-5',
    'claude-3-opus-20240229', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307'
  ],
  'Google': [
    'gemini-3-pro-preview',
    'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'gemini-2.5-pro',
    'gemini-2.0-flash', 'gemini-2.0-flash-lite'
  ],
  'Mistral': ['mistral-large-latest', 'mistral-small-latest', 'open-mixtral-8x7b'],
  'Cohere': [
    'command-a-03-2025', 'command-r7b-12-2024', 
    'command-a-translate-08-2025', 'command-a-reasoning-08-2025', 'command-a-vision-07-2025',
    'command-r-plus-08-2024', 'command-r-08-2024'
  ],
  'Groq': ['llama3-70b-8192', 'llama3-8b-8192', 'mixtral-8x7b-32768'],
  'Azure': ['gpt-4', 'gpt-35-turbo'], 
  'Hugging Face': ['meta-llama/Meta-Llama-3-70B', 'mistralai/Mixtral-8x7B-Instruct-v0.1']
};
