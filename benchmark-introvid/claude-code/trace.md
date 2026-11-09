# Plain Claude Code -- fresh run (Sonnet 5, 2026-11-08), no MCP, global CLAUDE.md excluded

Question: How does Excalidraw render and update canvas elements?

## 1. `Agent`

```json
{
 "description": "Research canvas rendering architecture",
 "prompt": "I need to explain to the user \"How does Excalidraw render and update canvas elements?\" This is for the excalidraw monorepo at C:\\work\\excalidraw.\n\nPlease research the rendering pipeline and report back with concrete file paths, key function/class names, and line numbers where relevant. Specifically investigate:\n\n1. Where the main canvas rendering logic lives (likely packages/excalidraw/renderer/ or similar) - what's the entry point for rendering the scene (e.g. renderScene, renderStaticScene, renderInteractiveScene or similar)?\n2. How elements are stored and managed (Scene class / elements map) - packages/excalidraw/scene/ \n3. The distinction between \"static\" canvas vs \"interactive\" canvas (if it exists) - e.g. separate canvases for selection/cursor overlays vs actual drawn elements.\n4. How updates are triggered - e.g. React state changes in App.tsx, requestAnimationFrame scheduling, throttling/rAF-batching utilities.\n5. How individual element types are drawn (shapes, text, images, freedraw) - look for a renderElement function and how it dispatches by element.type, and whether it uses an element \"shape\"/path cache (e.g. ShapeCache in packages/element).\n6. Any use of roughjs for hand-drawn rendering style.\n7. How the system decides what needs to be redrawed/invalidated (dirty checking, version numbers on elements, memoization).\n\nRead actual files (not just grep file names) to confirm function signatures and behavior. Report findings in a structured way with file_path:line_number references, organized under the headings above. Keep the report focused and under 600 words of prose (code references are fine beyond that implicitly).",
 "subagent_type": "Explore"
}
```
**result of 1**
```
Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)
agentId: aa9e10486941a80b3 (internal ID - do not mention to user. Use SendMessage with to: 'aa9e10486941a80b3', summary: '<5-10 word recap>' to continue this agent.)
The agent is working in the background. You will be notified automatically when it completes. You know nothing about its results until that notification arrives — do not report, assume, or predict them; continue other work or respond to the user in the meantime.
Do not duplicate this agent's work — avoid working with the same files or topics it is using.
output_file: C:\tmp\claude\C--work-excalidraw\4e328fd2-4322-4819-b698-8c7f0926d48b\tasks\aa9e10486941a80b3.output
Do NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification.
```

> I've kicked off research into Excalidraw's rendering pipeline — I'll summarize once it reports back.

## 2. `Bash` (sub-agent)

```json
{
 "command": "cd \"C:\\work\\excalidraw\" && find packages/excalidraw/renderer packages/excalidraw/scene packages/element -maxdepth 1 -type f 2>/dev/null | head -100",
 "description": "List renderer and scene directories"
}
```
## 3. `Glob` (sub-agent)

```json
{
 "pattern": "packages/excalidraw/renderer/**"
}
```
**result of 3**
```
packages\excalidraw\renderer\animation.ts
packages\excalidraw\renderer\helpers.test.ts
packages\excalidraw\renderer\helpers.ts
packages\excalidraw\renderer\interactiveScene.ts
packages\excalidraw\renderer\renderNewElementScene.ts
packages\excalidraw\renderer\renderSnaps.ts
packages\excalidraw\renderer\roundRect.ts
packages\excalidraw\renderer\staticScene.ts
packages\excalidraw\renderer\staticSvgScene.ts
```

## 4. `Glob` (sub-agent)

```json
{
 "pattern": "packages/excalidraw/scene/**"
}
```
**result of 4**
```
packages\excalidraw\scene\export.ts
packages\excalidraw\scene\index.ts
packages\excalidraw\scene\normalize.ts
packages\excalidraw\scene\Renderer.ts
packages\excalidraw\scene\scrollbars.ts
packages\excalidraw\scene\types.ts
```

**result of 2**
```
packages/excalidraw/renderer/animation.ts
packages/excalidraw/renderer/helpers.test.ts
packages/excalidraw/renderer/helpers.ts
packages/excalidraw/renderer/interactiveScene.ts
packages/excalidraw/renderer/renderNewElementScene.ts
packages/excalidraw/renderer/renderSnaps.ts
packages/excalidraw/renderer/roundRect.ts
packages/excalidraw/renderer/staticScene.ts
packages/excalidraw/renderer/staticSvgScene.ts
packages/excalidraw/scene/export.ts
packages/excalidraw/scene/index.ts
packages/excalidraw/scene/normalize.ts
packages/excalidraw/scene/Renderer.ts
packages/excalidraw/scene/scrollbars.ts
packages/excalidraw/scene/types.ts
packages/element/.eslintrc.json
packages/element/global.d.ts
packages/element/package.json
packages/element/README.md
packages/element/tsconfig.json
```

## 5. `Glob` (sub-agent)

```json
{
 "pattern": "packages/element/src/**"
}
```
**result of 5**
```
packages\element\src\align.ts
packages\element\src\arrowEndpointText.ts
packages\element\src\arrowheads.ts
packages\element\src\arrows\focus.ts
packages\element\src\arrows\helpers.ts
packages\element\src\binding.ts
packages\element\src\bounds.ts
packages\element\src\bucketFill.ts
packages\element\src\Scene.ts
packages\element\src\__tests__\transform.test.ts
packages\element\src\__tests__\__snapshots__\transform.test.ts.snap
packages\element\src\collision.ts
packages\element\src\comparisons.ts
packages\element\src\containerCache.ts
packages\element\src\convertToShape.ts
packages\element\src\cropElement.ts
packages\element\src\delta.ts
packages\element\src\distance.ts
packages\element\src\distribute.ts
packages\element\src\dragElements.ts
packages\element\src\duplicate.ts
packages\element\src\elbowArrow.ts
packages\element\src\elementLink.ts
packages\element\src\embeddable.ts
packages\element\src\flowchart.ts
packages\element\src\fractionalIndex.ts
packages\element\src\frame.ts
packages\element\src\groups.ts
packages\element\src\heading.ts
packages\element\src\image.ts
packages\element\src\index.ts
packages\element\src\linearElementEditor.ts
packages\element\src\mutateElement.ts
packages\element\src\newElement.ts
packages\element\src\positionElementsOnGrid.ts
packages\element\src\renderElement.ts
packages\element\src\resizeElements.ts
packages\element\src\resizeTest.ts
packages\element\src\selection.ts
packages\element\src\shape.ts
packages\element\src\showSelectedShapeActions.ts
packages\element\src\sizeHelpers.ts
packages\element\src\sortElements.ts
packages\element\src\store.ts
packages\element\src\textElement.ts
packages\element\src\textMeasurements.ts
packages\element\src\textWrapping.ts
packages\element\src\transform.ts
packages\element\src\transformHandles.ts
packages\element\src\typeChecks.ts
packages\element\src\types.ts
packages\element\src\utils.ts
packages\element\src\visualdebug.ts
packages\element\src\zindex.ts
```

## 6. `Read` (sub-agent)

```json
{
 "file_path": "C:\\work\\excalidraw\\packages\\excalidraw\\renderer\\staticScene.ts"
}
```
**result of 6**
```
1	import {
2	  applyDarkModeFilter,
3	  COLOR_WHITE,
4	  FRAME_STYLE,
5	  THEME,
6	  throttleRAF,
7	} from "@excalidraw/common";
8	import { isElementLink } from "@excalidraw/element";
9	import { createPlaceholderEmbeddableLabel } from "@excalidraw/element";
10	import { getBoundTextElement } from "@excalidraw/element";
11	import {
12	  isEmbeddableElement,
13	  isIframeLikeElement,
14	  isTextElement,
15	} from "@excalidraw/element";
16	import {
17	  elementOverlapsWithFrame,
18	  getTargetFrame,
19	  shouldApplyFrameClip,
20	} from "@excalidraw/element";
21	
22	import { renderElement } from "@excalidraw/element";
23	
24	import { getElementAbsoluteCoords } from "@excalidraw/element";
25	
26	import type {
27	  ElementsMap,
28	  ExcalidrawFrameLikeElement,
29	  NonDeletedExcalidrawElement,
30	} from "@excalidraw/element/types";
31	
32	import {
33	  EXTERNAL_LINK_IMG,
34	  ELEMENT_LINK_IMG,
35	  getLinkHandleFromCoords,
36	} from "../components/hyperlink/helpers";
37	
38	import {
39	  bootstrapCanvas,
40	  getNormalizedCanvasDimensions,
41	  snapScrollToDevicePixels,
42	} from "./helpers";
43	
44	import type {
45	  StaticCanvasRenderConfig,
46	  StaticSceneRenderConfig,
47	} from "../scene/types";
48	import type { StaticCanvasAppState, Zoom } from "../types";
49	
50	const GridLineColor = {
51	  [THEME.LIGHT]: {
52	    bold: "#dddddd",
53	    regular: "#e5e5e5",
54	  },
55	  [THEME.DARK]: {
56	    bold: applyDarkModeFilter("#dddddd"),
57	    regular: applyDarkModeFilter("#e5e5e5"),
58	  },
59	} as const;
60	
61	const strokeGrid = (
62	  context: CanvasRenderingContext2D,
63	  /** grid cell pixel size */
64	  gridSize: number,
65	  /** setting to 1 will disble bold lines */
66	  gridStep: number,
67	  scrollX: number,
68	  scrollY: number,
69	  zoom: Zoom,
70	  theme: StaticCanvasRenderConfig["theme"],
71	  width: number,
72	  height: number,
73	  scale: number,
74	) => {
75	  const offsetX = (scrollX % gridSize) - gridSize;
76	  const offsetY = (scrollY % gridSize) - gridSize;
77	
78	  const actualGridSize = gridSize * zoom.value;
79	
80	  const spaceWidth = 1 / zoom.value;
81	
82	  // scene units → device pixels
83	  const devicePixels = zoom.value * scale;
84	
85	  // A line at least a device pixel wide is drawn a whole number of device
86	  // pixels wide and centered to cover them exactly — on the half pixel when
87	  // the count is odd. Straddling a pixel boundary renders it as two lighter
88	  // pixels, which is how the grid looked at every zoom but 100%. Thinner
89	  // lines (zoomed far out) keep their sub-pixel width: their lightness is
90	  // the point.
91	  const snap = (position: number, maxWidthInCssPixels: number) => {
92	    // a line is `min(1 / zoom, max)` scene units wide; computed straight in
93	    // device pixels, so `(1 / zoom) × zoom` never lands just under 1
94	    const widthInDevicePixels = Math.min(
95	      scale,
96	      maxWidthInCssPixels * devicePixels,
97	    );
98	    if (widthInDevicePixels < 1) {
99	      return { position, lineWidth: widthInDevicePixels / devicePixels };
100	    }
101	    const wholeWidth = Math.round(widthInDevicePixels);
102	    const center = wholeWidth % 2 ? 0.5 : 0;
103	    return {
104	      position:
105	        (Math.round(position * devicePixels - center) + center) / devicePixels,
106	      lineWidth: wholeWidth / devicePixels,
107	    };
108	  };
109	
110	  context.save();
111	
112	  // vertical lines
113	  for (let x = offsetX; x < offsetX + width + gridSize * 2; x += gridSize) {
114	    const isBold =
115	      gridStep > 1 && Math.round(x - scrollX) % (gridStep * gridSize) === 0;
116	    // don't render regular lines when zoomed out and they're barely visible
117	    if (!isBold && actualGridSize < 10) {
118	      continue;
119	    }
120	
121	    const { position, lineWidth } = snap(x, isBold ? 4 : 1);
122	    context.lineWidth = lineWidth;
123	    const lineDash = [lineWidth * 3, spaceWidth + (lineWidth + spaceWidth)];
124	
125	    context.beginPath();
126	    context.setLineDash(isBold ? [] : lineDash);
127	    context.strokeStyle = isBold
128	      ? GridLineColor[theme].bold
129	      : GridLineColor[theme].regular;
130	    context.moveTo(position, offsetY - gridSize);
131	    context.lineTo(position, Math.ceil(offsetY + height + gridSize * 2));
132	    context.stroke();
133	  }
134	
135	  for (let y = offsetY; y < offsetY + height + gridSize * 2; y += gridSize) {
136	    const isBold =
137	      gridStep > 1 && Math.round(y - scrollY) % (gridStep * gridSize) === 0;
138	    if (!isBold && actualGridSize < 10) {
139	      continue;
140	    }
141	
142	    const { position, lineWidth } = snap(y, isBold ? 4 : 1);
143	    context.lineWidth = lineWidth;
144	    const lineDash = [lineWidth * 3, spaceWidth + (lineWidth + spaceWidth)];
145	
146	    context.beginPath();
147	    context.setLineDash(isBold ? [] : lineDash);
148	    context.strokeStyle = isBold
149	      ? GridLineColor[theme].bold
150	      : GridLineColor[theme].regular;
151	    context.moveTo(offsetX - gridSize, position);
152	    context.lineTo(Math.ceil(offsetX + width + gridSize * 2), position);
153	    context.stroke();
154	  }
155	  context.restore();
156	};
157	
158	export const frameClip = (
159	  frame: ExcalidrawFrameLikeElement,
160	  context: CanvasRenderingContext2D,
161	  renderConfig: StaticCanvasRenderConfig,
162	  appState: StaticCanvasAppState,
163	) => {
164	  context.translate(frame.x + appState.scrollX, frame.y + appState.scrollY);
165	  context.beginPath();
166	  if (context.roundRect) {
167	    context.roundRect(
168	      0,
169	      0,
170	      frame.width,
171	      frame.height,
172	      FRAME_STYLE.radius / appState.zoom.value,
173	    );
174	  } else {
175	    context.rect(0, 0, frame.width, frame.height);
176	  }
177	  context.clip();
178	  context.translate(
179	    -(frame.x + appState.scrollX),
180	    -(frame.y + appState.scrollY),
181	  );
182	};
183	
184	type LinkIconCanvas = HTMLCanvasElement & { zoom: number };
185	
186	const linkIconCanvasCache: {
187	  regularLink: LinkIconCanvas | null;
188	  elementLink: LinkIconCanvas | null;
189	} = {
190	  regularLink: null,
191	  elementLink: null,
192	};
193	
194	const renderLinkIcon = (
195	  element: NonDeletedExcalidrawElement,
196	  context: CanvasRenderingContext2D,
197	  appState: StaticCanvasAppState,
198	  elementsMap: ElementsMap,
199	) => {
200	  if (element.link && !appState.selectedElementIds[element.id]) {
201	    const [x1, y1, x2, y2] = getElementAbsoluteCoords(element, elementsMap);
202	    const [x, y, width, height] = getLinkHandleFromCoords(
203	      [x1, y1, x2, y2],
204	      element.angle,
205	      appState,
206	    );
207	    const centerX = x + width / 2;
208	    const centerY = y + height / 2;
209	    context.save();
210	    context.translate(appState.scrollX + centerX, appState.scrollY + centerY);
211	    context.rotate(element.angle);
212	
213	    const canvasKey = isElementLink(element.link)
214	      ? "elementLink"
215	      : "regularLink";
216	
217	    let linkCanvas = linkIconCanvasCache[canvasKey];
218	
219	    if (!linkCanvas || linkCanvas.zoom !== appState.zoom.value) {
220	      linkCanvas = Object.assign(document.createElement("canvas"), {
221	        zoom: appState.zoom.value,
222	      });
223	      linkCanvas.width = width * window.devicePixelRatio * appState.zoom.value;
224	      linkCanvas.height =
225	        height * window.devicePixelRatio * appState.zoom.value;
226	      linkIconCanvasCache[canvasKey] = linkCanvas;
227	
228	      const linkCanvasCacheContext = linkCanvas.getContext("2d")!;
229	      linkCanvasCacheContext.scale(
230	        window.devicePixelRatio * appState.zoom.value,
231	        window.devicePixelRatio * appState.zoom.value,
232	      );
233	
234	      // Seed a sane default so a corrupted color (silently rejected by the
235	      // canvas) falls back to white instead of a stale fillStyle.
236	      linkCanvasCacheContext.fillStyle = COLOR_WHITE;
237	      linkCanvasCacheContext.fillStyle =
238	        appState.viewBackgroundColor || COLOR_WHITE;
239	
240	      linkCanvasCacheContext.fillRect(0, 0, width, height);
241	
242	      if (canvasKey === "elementLink") {
243	        linkCanvasCacheContext.drawImage(ELEMENT_LINK_IMG, 0, 0, width, height);
244	      } else {
245	        linkCanvasCacheContext.drawImage(
246	          EXTERNAL_LINK_IMG,
247	          0,
248	          0,
249	          width,
250	          height,
251	        );
252	      }
253	
254	      linkCanvasCacheContext.restore();
255	    }
256	    context.globalAlpha = element.opacity / 100;
257	    context.drawImage(linkCanvas, x - centerX, y - centerY, width, height);
258	    context.restore();
259	  }
260	};
261	const _renderStaticScene = ({
262	  canvas,
263	  rc,
264	  elementsMap,
265	  allElementsMap,
266	  visibleElements,
267	  scale,
268	  appState: unsnappedAppState,
269	  renderConfig,
270	}: StaticSceneRenderConfig) => {
271	  if (canvas === null) {
272	    return;
273	  }
274	
275	  const { renderGrid = true, isExporting } = renderConfig;
276	  // export draws vectors, not cached bitmaps — nothing to keep on the grid
277	  const appState = isExporting
278	    ? unsnappedAppState
279	    : snapScrollToDevicePixels(unsnappedAppState, scale);
280	
281	  const [normalizedWidth, normalizedHeight] = getNormalizedCanvasDimensions(
282	    canvas,
283	    scale,
284	  );
285	
286	  const context = bootstrapCanvas({
287	    canvas,
288	    scale,
289	    normalizedWidth,
290	    normalizedHeight,
291	    theme: appState.theme,
292	    isExporting,
293	    viewBackgroundColor: appState.viewBackgroundColor,
294	  });
295	
296	  // Apply zoom
297	  context.scale(appState.zoom.value, appState.zoom.value);
298	
299	  // Grid
300	  if (renderGrid) {
301	    strokeGrid(
302	      context,
303	      appState.gridSize,
304	      appState.gridStep,
305	      appState.scrollX,
306	      appState.scrollY,
307	      appState.zoom,
308	      renderConfig.theme,
309	      normalizedWidth / appState.zoom.value,
310	      normalizedHeight / appState.zoom.value,
311	      scale,
312	    );
313	  }
314	
315	  const groupsToBeAddedToFrame = new Set<string>();
316	
317	  visibleElements.forEach((element) => {
318	    if (
319	      element.groupIds.length > 0 &&
320	      appState.frameToHighlight &&
321	      appState.selectedElementIds[element.id] &&
322	      (elementOverlapsWithFrame(
323	        element,
324	        appState.frameToHighlight,
325	        elementsMap,
326	      ) ||
327	        element.groupIds.find((groupId) => groupsToBeAddedToFrame.has(groupId)))
328	    ) {
329	      element.groupIds.forEach((groupId) =>
330	        groupsToBeAddedToFrame.add(groupId),
331	      );
332	    }
333	  });
334	
335	  const inFrameGroupsMap = new Map<string, boolean>();
336	
337	  // Paint visible elements
338	  visibleElements
339	    .filter((el) => !isIframeLikeElement(el))
340	    .forEach((element) => {
341	      try {
342	        const frameId = element.frameId || appState.frameToHighlight?.id;
343	
344	        if (
345	          isTextElement(element) &&
346	          element.containerId &&
347	          elementsMap.has(element.containerId)
348	        ) {
349	          // will be rendered with the container
350	          return;
351	        }
352	
353	        context.save();
354	
355	        if (
356	          frameId &&
357	          appState.frameRendering.enabled &&
358	          appState.frameRendering.clip
359	        ) {
360	          const frame = getTargetFrame(element, elementsMap, appState);
361	          if (
362	            frame &&
363	            shouldApplyFrameClip(
364	              element,
365	              frame,
366	              appState,
367	              elementsMap,
368	              inFrameGroupsMap,
369	            )
370	          ) {
371	            frameClip(frame, context, renderConfig, appState);
372	          }
373	          renderElement(
374	            element,
375	            elementsMap,
376	            allElementsMap,
377	            rc,
378	            context,
379	            renderConfig,
380	            appState,
381	          );
382	        } else {
383	          renderElement(
384	            element,
385	            elementsMap,
386	            allElementsMap,
387	            rc,
388	            context,
389	            renderConfig,
390	            appState,
391	          );
392	        }
393	
394	        const boundTextElement = getBoundTextElement(element, elementsMap);
395	        if (boundTextElement) {
396	          renderElement(
397	            boundTextElement,
398	            elementsMap,
399	            allElementsMap,
400	            rc,
401	            context,
402	            renderConfig,
403	            appState,
404	          );
405	        }
406	
407	        context.restore();
408	
409	        if (!isExporting && renderConfig.renderLinks !== false) {
410	          renderLinkIcon(element, context, appState, elementsMap);
411	        }
412	      } catch (error: any) {
413	        console.error(
414	          error,
415	          element.id,
416	          element.x,
417	          element.y,
418	          element.width,
419	          element.height,
420	        );
421	      }
422	    });
423	
424	  // render embeddables on top
425	  visibleElements
426	    .filter((el) => isIframeLikeElement(el))
427	    .forEach((element) => {
428	      try {
429	        const render = () => {
430	          renderElement(
431	            element,
432	            elementsMap,
433	            allElementsMap,
434	            rc,
435	            context,
436	            renderConfig,
437	            appState,
438	          );
439	
440	          if (
441	            isIframeLikeElement(element) &&
442	            (isExporting ||
443	              (isEmbeddableElement(element) &&
444	                renderConfig.embedsValidationStatus.get(element.id) !==
445	                  true)) &&
446	            element.width &&
447	            element.height
448	          ) {
449	            const label = createPlaceholderEmbeddableLabel(element);
450	            renderElement(
451	              label,
452	              elementsMap,
453	              allElementsMap,
454	              rc,
455	              context,
456	              renderConfig,
457	              appState,
458	            );
459	          }
460	          if (!isExporting && renderConfig.renderLinks !== false) {
461	            renderLinkIcon(element, context, appState, elementsMap);
462	          }
463	        };
464	        // - when exporting the whole canvas, we DO NOT apply clipping
465	        // - when we are exporting a particular frame, apply clipping
466	        //   if the containing frame is not selected, apply clipping
467	        const frameId = element.frameId || appState.frameToHighlight?.id;
468	
469	        if (
470	          frameId &&
471	          appState.frameRendering.enabled &&
472	          appState.frameRendering.clip
473	        ) {
474	          context.save();
475	
476	          const frame = getTargetFrame(element, elementsMap, appState);
477	
478	          if (
479	            frame &&
480	            shouldApplyFrameClip(
481	              element,
482	              frame,
483	              appState,
484	              elementsMap,
485	              inFrameGroupsMap,
486	            )
487	          ) {
488	            frameClip(frame, context, renderConfig, appState);
489	          }
490	          render();
491	          context.restore();
492	        } else {
493	          render();
494	        }
495	      } catch (error: any) {
496	        console.error(error);
497	      }
498	    });
499	
500	  // render pending nodes for flowcharts
501	  renderConfig.pendingFlowchartNodes?.forEach((element) => {
502	    try {
503	      renderElement(
504	        element,
505	        elementsMap,
506	        allElementsMap,
507	        rc,
508	        context,
509	        renderConfig,
510	        appState,
511	      );
512	    } catch (error) {
513	      console.error(error);
514	    }
515	  });
516	};
517	
518	/** throttled to animation framerate */
519	export const renderStaticSceneThrottled = throttleRAF(
520	  (config: StaticSceneRenderConfig) => {
521	    _renderStaticScene(config);
522	  },
523	);
524	
525	/**
526	 * Static scene is the non-ui canvas where we render elements.
527	 */
528	export const renderStaticScene = (
529	  renderConfig: StaticSceneRenderConfig,
530	  throttle?: boolean,
531	) => {
532	  if (throttle) {
533	    renderStaticSceneThrottled(renderConfig);
534	    return;
535	  }
536	
537	  _renderStaticScene(renderConfig);
538	};
539	
```

## 7. `Read` (sub-agent)

```json
{
 "file_path": "C:\\work\\excalidraw\\packages\\excalidraw\\renderer\\interactiveScene.ts",
 "limit": 150
}
```
**result of 7**
```
1	import {
2	  clamp,
3	  pointFrom,
4	  pointsEqual,
5	  type GlobalPoint,
6	  type LocalPoint,
7	  type Radians,
8	  bezierEquation,
9	  pointRotateRads,
10	  pointDistance,
11	} from "@excalidraw/math";
12	
13	import {
14	  arrayToMap,
15	  BIND_MODE_TIMEOUT,
16	  DEFAULT_TRANSFORM_HANDLE_SPACING,
17	  FRAME_STYLE,
18	  getFeatureFlag,
19	  invariant,
20	  shouldRotateWithDiscreteAngle,
21	  THEME,
22	  applyDarkModeFilter,
23	} from "@excalidraw/common";
24	
25	import {
26	  deconstructDiamondElement,
27	  deconstructRectanguloidElement,
28	  elementCenterPoint,
29	  getDiamondBaseCorners,
30	  FOCUS_POINT_SIZE,
31	  getOmitSidesForEditorInterface,
32	  getTransformHandles,
33	  getTransformHandlesFromCoords,
34	  hasBoundingBox,
35	  hitElementItself,
36	  isArrowElement,
37	  isBindableElement,
38	  isElbowArrow,
39	  isFrameLikeElement,
40	  isImageElement,
41	  isLinearElement,
42	  isLineElement,
43	  maxBindingDistance_simple,
44	  isTextElement,
45	  LinearElementEditor,
46	  getActiveTextElement,
47	  getElementsInGroup,
48	  getSelectedGroupIds,
49	  isSelectedViaGroup,
50	  selectGroupsFromGivenElements,
51	} from "@excalidraw/element";
52	
53	import { renderSelectionElement } from "@excalidraw/element";
54	
55	import { getCommonBounds, getElementAbsoluteCoords } from "@excalidraw/element";
56	import {
57	  getGlobalFixedPointForBindableElement,
58	  isFocusPointVisible,
59	} from "@excalidraw/element";
60	
61	import type { EditorInterface } from "@excalidraw/common";
62	
63	import type {
64	  TransformHandles,
65	  TransformHandleType,
66	} from "@excalidraw/element";
67	
68	import type {
69	  ElementsMap,
70	  ExcalidrawArrowElement,
71	  ExcalidrawBindableElement,
72	  ExcalidrawElement,
73	  ExcalidrawFrameLikeElement,
74	  ExcalidrawImageElement,
75	  ExcalidrawLinearElement,
76	  ExcalidrawTextElement,
77	  GroupId,
78	  NonDeleted,
79	  NonDeletedExcalidrawElement,
80	  NonDeletedSceneElementsMap,
81	} from "@excalidraw/element/types";
82	
83	import { renderSnaps } from "../renderer/renderSnaps";
84	import { roundRect } from "../renderer/roundRect";
85	import {
86	  getScrollBars,
87	  SCROLLBAR_COLOR,
88	  SCROLLBAR_WIDTH,
89	} from "../scene/scrollbars";
90	
91	import { getClientColor, renderRemoteCursors } from "../clients";
92	import {
93	  getTextAutoResizeHandle,
94	  getTextBoxPadding,
95	} from "../textAutoResizeHandle";
96	
97	import {
98	  bootstrapCanvas,
99	  fillCircle,
100	  getNormalizedCanvasDimensions,
101	  strokeRectWithRotation_simple,
102	  snapScrollToDevicePixels,
103	} from "./helpers";
104	
105	import type {
106	  AppState,
107	  AppClassProperties,
108	  InteractiveCanvasAppState,
109	} from "../types";
110	import type {
111	  InteractiveCanvasRenderConfig,
112	  InteractiveSceneRenderConfig,
113	  RenderableElementsMap,
114	} from "../scene/types";
115	
116	// The interactive canvas used to be inverted in dark mode via a CSS filter
117	// (`invert(93%) hue-rotate(180deg)`), which is prohibitively slow in browsers
118	// that composite in software (e.g. Firefox on software WebRender). We now map
119	// the colors in JS instead (see `applyDarkModeFilter`), so the dark-mode
120	// values below are the post-filter equivalents of the previous ones.
121	// ---------------------------------------------------------------------------
122	
123	const BINDING_HIGHLIGHT_RGB = {
124	  [THEME.LIGHT]: "106, 189, 252",
125	  [THEME.DARK]: "104, 182, 240",
126	} as const;
127	
128	const BINDING_MIDPOINT_COLOR = {
129	  [THEME.LIGHT]: "rgba(65, 65, 65, 0.5)",
130	  [THEME.DARK]: "rgba(237, 237, 237, 0.8)",
131	} as const;
132	
133	const SEARCH_MATCH_COLOR = {
134	  [THEME.LIGHT]: {
135	    focus: "rgba(255, 124, 0, 0.4)",
136	    match: "rgba(255, 226, 0, 0.4)",
137	  },
138	  [THEME.DARK]: {
139	    focus: "rgba(250, 123, 53, 0.4)",
140	    match: "rgba(221, 181, 136, 0.4)",
141	  },
142	} as const;
143	
144	/** maps a light-mode UI color to its dark-mode counterpart when in dark mode */
145	const getThemedColor = (
146	  color: string,
147	  theme: InteractiveCanvasAppState["theme"],
148	) => applyDarkModeFilter(color, theme === THEME.DARK);
149	
150	const renderElbowArrowMidPointHighlight = (
```

## 8. `Bash` (sub-agent)

```json
{
 "command": "cd \"C:\\work\\excalidraw\" && grep -n \"renderInteractiveSceneThrottled\\|export const _renderInteractiveScene\\|export const renderInteractiveScene\" packages/excalidraw/renderer/interactiveScene.ts | tail -30",
 "description": "Find interactive scene export functions"
}
```
**result of 8**
```
2165:export const renderInteractiveScene = <
```

## 9. `Read` (sub-agent)

```json
{
 "file_path": "C:\\work\\excalidraw\\packages\\excalidraw\\scene\\Renderer.ts"
}
```
**result of 9**
```
1	import {
2	  getCommonFrameId,
3	  getFrameChildrenInsertionIndex,
4	  isElementInViewport,
5	} from "@excalidraw/element";
6	
7	import { arrayToMap, memoize, toBrandedType } from "@excalidraw/common";
8	
9	import type {
10	  ExcalidrawElement,
11	  ExcalidrawFrameLikeElement,
12	  NonDeleted,
13	  NonDeletedElementsMap,
14	  NonDeletedExcalidrawElement,
15	} from "@excalidraw/element/types";
16	
17	import type { Scene } from "@excalidraw/element";
18	
19	import { renderStaticSceneThrottled } from "../renderer/staticScene";
20	
21	import type { RenderableElementsMap } from "./types";
22	
23	import type { AppState } from "../types";
24	
25	type GetRenderableElementsOpts = {
26	  zoom: AppState["zoom"];
27	  offsetLeft: AppState["offsetLeft"];
28	  offsetTop: AppState["offsetTop"];
29	  scrollX: AppState["scrollX"];
30	  scrollY: AppState["scrollY"];
31	  height: AppState["height"];
32	  width: AppState["width"];
33	  editingTextElement: AppState["editingTextElement"];
34	  newElement: AppState["newElement"];
35	  selectedElements: readonly NonDeletedExcalidrawElement[];
36	  selectedElementsAreBeingDragged: AppState["selectedElementsAreBeingDragged"];
37	  frameToHighlight: AppState["frameToHighlight"];
38	};
39	
40	export class Renderer {
41	  private scene: Scene;
42	
43	  constructor(scene: Scene) {
44	    this.scene = scene;
45	  }
46	
47	  private getVisibleCanvasElements({
48	    elementsMap,
49	    zoom,
50	    offsetLeft,
51	    offsetTop,
52	    scrollX,
53	    scrollY,
54	    height,
55	    width,
56	  }: {
57	    elementsMap: NonDeletedElementsMap;
58	    zoom: AppState["zoom"];
59	    offsetLeft: AppState["offsetLeft"];
60	    offsetTop: AppState["offsetTop"];
61	    scrollX: AppState["scrollX"];
62	    scrollY: AppState["scrollY"];
63	    height: AppState["height"];
64	    width: AppState["width"];
65	  }): readonly NonDeletedExcalidrawElement[] {
66	    const visibleElements: NonDeletedExcalidrawElement[] = [];
67	    for (const element of elementsMap.values()) {
68	      if (
69	        isElementInViewport(
70	          element,
71	          width,
72	          height,
73	          {
74	            zoom,
75	            offsetLeft,
76	            offsetTop,
77	            scrollX,
78	            scrollY,
79	          },
80	          elementsMap,
81	        )
82	      ) {
83	        visibleElements.push(element);
84	      }
85	    }
86	    return visibleElements;
87	  }
88	
89	  private getRenderableElementsMap({
90	    elements,
91	    editingTextElement,
92	    newElement,
93	  }: {
94	    elements: readonly NonDeletedExcalidrawElement[];
95	    editingTextElement: AppState["editingTextElement"];
96	    newElement: AppState["newElement"];
97	  }) {
98	    const elementsMap = toBrandedType<RenderableElementsMap>(new Map());
99	    const newElementCanvasElement = newElement?.frameId ? null : newElement;
100	
101	    for (const element of elements) {
102	      if (newElementCanvasElement?.id === element.id) {
103	        continue;
104	      }
105	
106	      // we don't want to render text element that's being currently edited
107	      // (it's rendered on remote only)
108	      if (
109	        !editingTextElement ||
110	        editingTextElement.type !== "text" ||
111	        element.id !== editingTextElement.id
112	      ) {
113	        elementsMap.set(element.id, element);
114	      }
115	    }
116	    return { elementsMap, newElementCanvasElement };
117	  }
118	
119	  private sortSelectedElementsIntoHighlightedFrame<
120	    T extends ExcalidrawElement,
121	  >({
122	    visibleElements,
123	    selectedElements,
124	    frameToHighlight,
125	  }: {
126	    selectedElements: readonly NonDeletedExcalidrawElement[];
127	    visibleElements: readonly T[];
128	    frameToHighlight: NonDeleted<ExcalidrawFrameLikeElement>;
129	  }): readonly T[] {
130	    if (!selectedElements.length) {
131	      return visibleElements;
132	    }
133	
134	    // we assume all selected elements are eligible frame children if
135	    // frameToHighlight is defined
136	    const selectedElementsMap = arrayToMap(selectedElements);
137	
138	    // thus, all deselected elements are the ones we won't reorder
139	    const deselectedElements = visibleElements.filter(
140	      (element) => !selectedElementsMap.has(element.id),
141	    );
142	
143	    const insertionIndex = getFrameChildrenInsertionIndex(
144	      deselectedElements,
145	      frameToHighlight.id,
146	    );
147	
148	    if (insertionIndex === null) {
149	      return visibleElements;
150	    }
151	
152	    return [
153	      ...deselectedElements.slice(0, insertionIndex),
154	      ...selectedElements,
155	      ...deselectedElements.slice(insertionIndex),
156	    ] as readonly T[];
157	  }
158	
159	  private _getRenderableElements = memoize(
160	    ({
161	      canvasNonce,
162	      zoom,
163	      offsetLeft,
164	      offsetTop,
165	      scrollX,
166	      scrollY,
167	      height,
168	      width,
169	      editingTextElement,
170	      newElement,
171	    }: Omit<
172	      GetRenderableElementsOpts,
173	      | "selectedElements"
174	      | "selectedElementsAreBeingDragged"
175	      | "frameToHighlight"
176	    > & {
177	      canvasNonce: string;
178	    }) => {
179	      const elements = this.scene.getNonDeletedElements();
180	
181	      const { elementsMap, newElementCanvasElement } =
182	        this.getRenderableElementsMap({
183	          elements,
184	          editingTextElement,
185	          newElement,
186	        });
187	
188	      const visibleElements = this.getVisibleCanvasElements({
189	        elementsMap,
190	        zoom,
191	        offsetLeft,
192	        offsetTop,
193	        scrollX,
194	        scrollY,
195	        height,
196	        width,
197	      });
198	
199	      return {
200	        elementsMap,
201	        visibleElements,
202	        newElementCanvasElement,
203	        canvasNonce,
204	      };
205	    },
206	  );
207	
208	  public getRenderableElements = (opts: GetRenderableElementsOpts) => {
209	    const { newElement } = opts;
210	    const canvasNonce = `${this.scene.getSceneNonce()}${
211	      newElement?.frameId ? `:${newElement.versionNonce}` : ""
212	    }`;
213	
214	    const ret = this._getRenderableElements({
215	      canvasNonce,
216	
217	      // don't spread `opts` because we don't want to memoize on some props
218	
219	      zoom: opts.zoom,
220	      offsetLeft: opts.offsetLeft,
221	      offsetTop: opts.offsetTop,
222	      scrollX: opts.scrollX,
223	      scrollY: opts.scrollY,
224	      height: opts.height,
225	      width: opts.width,
226	      editingTextElement: opts.editingTextElement,
227	      newElement: opts.newElement,
228	    });
229	
230	    // if we're dragging elements over a frame, reorder the selected elements
231	    // inside the frame during render (we don't set the `element.frameId` until
232	    // pointerup else we'd have to painstainly restore the orig index if user
233	    // didn't end up adding elements to the frame)
234	    if (
235	      opts.frameToHighlight &&
236	      opts.selectedElementsAreBeingDragged &&
237	      // if all dragged elements are already in the frame, don't reorder
238	      getCommonFrameId(opts.selectedElements) !== opts.frameToHighlight.id
239	    ) {
240	      const reorderedVisibleElements =
241	        this.sortSelectedElementsIntoHighlightedFrame({
242	          visibleElements: ret.visibleElements,
243	          selectedElements: opts.selectedElements,
244	          frameToHighlight: opts.frameToHighlight,
245	        });
246	
247	      return {
248	        ...ret,
249	        visibleElements: reorderedVisibleElements,
250	      };
251	    }
252	
253	    return ret;
254	  };
255	
256	  // NOTE Doesn't destroy everything (scene, rc, etc.) because it may not be
257	  // safe to break TS contract here (for upstream cases)
258	  public destroy() {
259	    renderStaticSceneThrottled.cancel();
260	    this._getRenderableElements.clear();
261	  }
262	}
263	
```

## 10. `Read` (sub-agent)

```json
{
 "file_path": "C:\\work\\excalidraw\\packages\\element\\src\\shape.ts"
}
```
**result of 10**
```
1	import { simplify } from "points-on-curve";
2	import { getStroke, getStrokePoints } from "perfect-freehand";
3	import { LaserPointer } from "@excalidraw/laser-pointer";
4	
5	import {
6	  type GeometricShape,
7	  getClosedCurveShape,
8	  getCurveShape,
9	  getEllipseShape,
10	  getFreedrawShape,
11	  getPolygonShape,
12	} from "@excalidraw/utils/shape";
13	
14	import {
15	  pointFrom,
16	  pointDistance,
17	  type LocalPoint,
18	  pointRotateRads,
19	} from "@excalidraw/math";
20	import {
21	  ROUGHNESS,
22	  THEME,
23	  isTransparent,
24	  assertNever,
25	  COLOR_PALETTE,
26	  LINE_POLYGON_POINT_MERGE_DISTANCE,
27	  applyDarkModeFilter,
28	  DEFAULT_STROKE_STREAMLINE,
29	} from "@excalidraw/common";
30	
31	import { RoughGenerator } from "roughjs/bin/generator";
32	
33	import type { GlobalPoint } from "@excalidraw/math";
34	
35	import type { Mutable } from "@excalidraw/common/utility-types";
36	
37	import type {
38	  AppState,
39	  EmbedsValidationStatus,
40	} from "@excalidraw/excalidraw/types";
41	import type {
42	  ElementShape,
43	  ElementShapes,
44	  SVGPathString,
45	} from "@excalidraw/excalidraw/scene/types";
46	
47	import { elementWithCanvasCache } from "./renderElement";
48	
49	import {
50	  canBecomePolygon,
51	  isElbowArrow,
52	  isEmbeddableElement,
53	  isIframeElement,
54	  isIframeLikeElement,
55	  isLinearElement,
56	} from "./typeChecks";
57	import { getCornerRadius, isPathALoop } from "./utils";
58	import { headingForPointIsHorizontal } from "./heading";
59	
60	import { canChangeRoundness } from "./comparisons";
61	import {
62	  elementCenterPoint,
63	  getArrowheadPoints,
64	  getDiamondPoints,
65	  getElementAbsoluteCoords,
66	} from "./bounds";
67	import { shouldTestInside } from "./collision";
68	
69	import type {
70	  ExcalidrawElement,
71	  ExcalidrawSelectionElement,
72	  ExcalidrawLinearElement,
73	  ExcalidrawFreeDrawElement,
74	  ElementsMap,
75	  ExcalidrawLineElement,
76	  Arrowhead,
77	} from "./types";
78	
79	import type { Drawable, Options } from "roughjs/bin/core";
80	import type { Point as RoughPoint } from "roughjs/bin/geometry";
81	
82	export class ShapeCache {
83	  private static rg = new RoughGenerator();
84	  private static cache = new WeakMap<
85	    ExcalidrawElement,
86	    { shape: ElementShape; theme: AppState["theme"] }
87	  >();
88	
89	  /**
90	   * Retrieves shape from cache if available. Use this only if shape
91	   * is optional and you have a fallback in case it's not cached.
92	   */
93	  public static get = <T extends ExcalidrawElement>(
94	    element: T,
95	    theme: AppState["theme"] | null,
96	  ) => {
97	    const cached = ShapeCache.cache.get(element);
98	    if (cached && (theme === null || cached.theme === theme)) {
99	      return cached.shape as T["type"] extends keyof ElementShapes
100	        ? ElementShapes[T["type"]] | undefined
101	        : ElementShape | undefined;
102	    }
103	    return undefined;
104	  };
105	
106	  public static delete = (element: ExcalidrawElement) => {
107	    ShapeCache.cache.delete(element);
108	    elementWithCanvasCache.delete(element);
109	  };
110	
111	  public static destroy = () => {
112	    ShapeCache.cache = new WeakMap();
113	  };
114	
115	  /**
116	   * Generates & caches shape for element if not already cached, otherwise
117	   * returns cached shape.
118	   */
119	  public static generateElementShape = <
120	    T extends Exclude<ExcalidrawElement, ExcalidrawSelectionElement>,
121	  >(
122	    element: T,
123	    renderConfig: {
124	      isExporting: boolean;
125	      canvasBackgroundColor: AppState["viewBackgroundColor"];
126	      embedsValidationStatus: EmbedsValidationStatus;
127	      theme: AppState["theme"];
128	    } | null,
129	  ) => {
130	    // when exporting, always regenerated to guarantee the latest shape
131	    const cachedShape = renderConfig?.isExporting
132	      ? undefined
133	      : ShapeCache.get(element, renderConfig ? renderConfig.theme : null);
134	
135	    // `null` indicates no rc shape applicable for this element type,
136	    // but it's considered a valid cache value (= do not regenerate)
137	    if (cachedShape !== undefined) {
138	      return cachedShape;
139	    }
140	
141	    elementWithCanvasCache.delete(element);
142	
143	    const shape = _generateElementShape(
144	      element,
145	      ShapeCache.rg,
146	      renderConfig || {
147	        isExporting: false,
148	        canvasBackgroundColor: COLOR_PALETTE.white,
149	        embedsValidationStatus: null,
150	        theme: THEME.LIGHT,
151	      },
152	    ) as T["type"] extends keyof ElementShapes
153	      ? ElementShapes[T["type"]]
154	      : Drawable | null;
155	
156	    if (!renderConfig?.isExporting) {
157	      ShapeCache.cache.set(element, {
158	        shape,
159	        theme: renderConfig?.theme || THEME.LIGHT,
160	      });
161	    }
162	
163	    return shape;
164	  };
165	}
166	
167	const getDashArrayDashed = (strokeWidth: number) => [8, 8 + strokeWidth];
168	
169	const getDashArrayDotted = (strokeWidth: number) => [1.5, 6 + strokeWidth];
170	
171	function adjustRoughness(element: ExcalidrawElement): number {
172	  const roughness = element.roughness;
173	
174	  const maxSize = Math.max(element.width, element.height);
175	  const minSize = Math.min(element.width, element.height);
176	
177	  // don't reduce roughness if
178	  if (
179	    // both sides relatively big
180	    (minSize >= 20 && maxSize >= 50) ||
181	    // is round & both sides above 15px
182	    (minSize >= 15 &&
183	      !!element.roundness &&
184	      canChangeRoundness(element.type)) ||
185	    // relatively long linear element
186	    (isLinearElement(element) && maxSize >= 50)
187	  ) {
188	    return roughness;
189	  }
190	
191	  return Math.min(roughness / (maxSize < 10 ? 3 : 2), 2.5);
192	}
193	
194	export const generateRoughOptions = (
195	  element: ExcalidrawElement,
196	  continuousPath = false,
197	  isDarkMode: boolean = false,
198	): Options => {
199	  const options: Options = {
200	    seed: element.seed,
201	    strokeLineDash:
202	      element.strokeStyle === "dashed"
203	        ? getDashArrayDashed(element.strokeWidth)
204	        : element.strokeStyle === "dotted"
205	        ? getDashArrayDotted(element.strokeWidth)
206	        : undefined,
207	    // for non-solid strokes, disable multiStroke because it tends to make
208	    // dashes/dots overlay each other
209	    disableMultiStroke: element.strokeStyle !== "solid",
210	    // for non-solid strokes, increase the width a bit to make it visually
211	    // similar to solid strokes, because we're also disabling multiStroke
212	    strokeWidth:
213	      element.strokeStyle !== "solid"
214	        ? element.strokeWidth + 0.5
215	        : element.strokeWidth,
216	    // when increasing strokeWidth, we must explicitly set fillWeight and
217	    // hachureGap because if not specified, roughjs uses strokeWidth to
218	    // calculate them (and we don't want the fills to be modified)
219	    fillWeight: element.strokeWidth / 2,
220	    hachureGap: element.strokeWidth * 4,
221	    roughness: adjustRoughness(element),
222	    stroke: applyDarkModeFilter(element.strokeColor, isDarkMode),
223	    preserveVertices:
224	      continuousPath || element.roughness < ROUGHNESS.cartoonist,
225	  };
226	
227	  switch (element.type) {
228	    case "rectangle":
229	    case "iframe":
230	    case "embeddable":
231	    case "diamond":
232	    case "ellipse": {
233	      options.fillStyle = element.fillStyle;
234	      options.fill = isTransparent(element.backgroundColor)
235	        ? undefined
236	        : applyDarkModeFilter(element.backgroundColor, isDarkMode);
237	      if (element.type === "ellipse") {
238	        options.curveFitting = 1;
239	      }
240	      return options;
241	    }
242	    case "line":
243	    case "freedraw": {
244	      if (isPathALoop(element.points)) {
245	        options.fillStyle = element.fillStyle;
246	        options.fill =
247	          element.backgroundColor === "transparent"
248	            ? undefined
249	            : applyDarkModeFilter(element.backgroundColor, isDarkMode);
250	      }
251	      return options;
252	    }
253	    case "arrow":
254	      return options;
255	    default: {
256	      throw new Error(`Unimplemented type ${element.type}`);
257	    }
258	  }
259	};
260	
261	const modifyIframeLikeForRoughOptions = (
262	  element: ExcalidrawElement,
263	  isExporting: boolean,
264	  embedsValidationStatus: EmbedsValidationStatus | null,
265	) => {
266	  if (
267	    isIframeLikeElement(element) &&
268	    (isExporting ||
269	      (isEmbeddableElement(element) &&
270	        embedsValidationStatus?.get(element.id) !== true)) &&
271	    isTransparent(element.backgroundColor) &&
272	    isTransparent(element.strokeColor)
273	  ) {
274	    return {
275	      ...element,
276	      roughness: 0,
277	      backgroundColor: "#d3d3d3",
278	      fillStyle: "solid",
279	    } as const;
280	  } else if (isIframeElement(element)) {
281	    return {
282	      ...element,
283	      strokeColor: isTransparent(element.strokeColor)
284	        ? "#000000"
285	        : element.strokeColor,
286	      backgroundColor: isTransparent(element.backgroundColor)
287	        ? "#f4f4f6"
288	        : element.backgroundColor,
289	    };
290	  }
291	  return element;
292	};
293	
294	const generateArrowheadCardinalityOne = (
295	  generator: RoughGenerator,
296	  arrowheadPoints: number[] | null,
297	  lineOptions: Options,
298	) => {
299	  if (arrowheadPoints === null) {
300	    return [];
301	  }
302	
303	  const [, , x3, y3, x4, y4] = arrowheadPoints;
304	
305	  return [generator.line(x3, y3, x4, y4, lineOptions)];
306	};
307	
308	const generateArrowheadLinesToTip = (
309	  generator: RoughGenerator,
310	  arrowheadPoints: number[] | null,
311	  lineOptions: Options,
312	) => {
313	  if (arrowheadPoints === null) {
314	    return [];
315	  }
316	
317	  const [x2, y2, x3, y3, x4, y4] = arrowheadPoints;
318	
319	  return [
320	    generator.line(x3, y3, x2, y2, lineOptions),
321	    generator.line(x4, y4, x2, y2, lineOptions),
322	  ];
323	};
324	
325	const getArrowheadLineOptions = (
326	  element: ExcalidrawLinearElement,
327	  options: Options,
328	) => {
329	  const lineOptions = { ...options };
330	
331	  if (element.strokeStyle === "dotted") {
332	    // for dotted arrows caps, reduce gap to make it more legible
333	    const dash = getDashArrayDotted(element.strokeWidth - 1);
334	    lineOptions.strokeLineDash = [dash[0], dash[1] - 1];
335	  } else {
336	    // for solid/dashed, keep solid arrow cap
337	    delete lineOptions.strokeLineDash;
338	  }
339	  lineOptions.roughness = Math.min(1, lineOptions.roughness || 0);
340	
341	  return lineOptions;
342	};
343	
344	const generateArrowheadOutlineCircle = (
345	  generator: RoughGenerator,
346	  options: Options,
347	  strokeColor: string,
348	  arrowheadPoints: number[] | null,
349	  fill: string,
350	  diameterScale = 1,
351	) => {
352	  if (arrowheadPoints === null) {
353	    return [];
354	  }
355	
356	  const [x, y, diameter] = arrowheadPoints;
357	  const circleOptions = {
358	    ...options,
359	    fill,
360	    fillStyle: "solid" as const,
361	    stroke: strokeColor,
362	    roughness: Math.min(0.5, options.roughness || 0),
363	  };
364	
365	  delete circleOptions.strokeLineDash;
366	
367	  return [generator.circle(x, y, diameter * diameterScale, circleOptions)];
368	};
369	
370	const getArrowheadShapes = (
371	  element: ExcalidrawLinearElement,
372	  shape: Drawable[],
373	  position: "start" | "end",
374	  arrowhead: Arrowhead,
375	  generator: RoughGenerator,
376	  options: Options,
377	  canvasBackgroundColor: string,
378	  isDarkMode: boolean,
379	) => {
380	  if (arrowhead === null) {
381	    return [];
382	  }
383	
384	  const strokeColor = applyDarkModeFilter(element.strokeColor, isDarkMode);
385	  const backgroundFillColor = applyDarkModeFilter(
386	    canvasBackgroundColor,
387	    isDarkMode,
388	  );
389	  const cardinalityOneOrManyOffset = -0.25;
390	  const cardinalityZeroCircleScale = 0.8;
391	
392	  switch (arrowhead) {
393	    case "circle":
394	    case "circle_outline": {
395	      return generateArrowheadOutlineCircle(
396	        generator,
397	        options,
398	        strokeColor,
399	        getArrowheadPoints(element, shape, position, arrowhead),
400	        arrowhead === "circle_outline" ? backgroundFillColor : strokeColor,
401	      );
402	    }
403	    case "triangle":
404	    case "triangle_outline": {
405	      const arrowheadPoints = getArrowheadPoints(
406	        element,
407	        shape,
408	        position,
409	        arrowhead,
410	      );
411	
412	      if (arrowheadPoints === null) {
413	        return [];
414	      }
415	
416	      const [x, y, x2, y2, x3, y3] = arrowheadPoints;
417	      const triangleOptions = {
418	        ...options,
419	        fill:
420	          arrowhead === "triangle_outline" ? backgroundFillColor : strokeColor,
421	        fillStyle: "solid" as const,
422	        roughness: Math.min(1, options.roughness || 0),
423	      };
424	
425	      // always use solid stroke for arrowhead
426	      delete triangleOptions.strokeLineDash;
427	
428	      return [
429	        generator.polygon(
430	          [
431	            [x, y],
432	            [x2, y2],
433	            [x3, y3],
434	            [x, y],
435	          ],
436	          triangleOptions,
437	        ),
438	      ];
439	    }
440	    case "diamond":
441	    case "diamond_outline": {
442	      const arrowheadPoints = getArrowheadPoints(
443	        element,
444	        shape,
445	        position,
446	        arrowhead,
447	      );
448	
449	      if (arrowheadPoints === null) {
450	        return [];
451	      }
452	
453	      const [x, y, x2, y2, x3, y3, x4, y4] = arrowheadPoints;
454	      const diamondOptions = {
455	        ...options,
456	        fill:
457	          arrowhead === "diamond_outline" ? backgroundFillColor : strokeColor,
458	        fillStyle: "solid" as const,
459	        roughness: Math.min(1, options.roughness || 0),
460	      };
461	
462	      // always use solid stroke for arrowhead
463	      delete diamondOptions.strokeLineDash;
464	
465	      return [
466	        generator.polygon(
467	          [
468	            [x, y],
469	            [x2, y2],
470	            [x3, y3],
471	            [x4, y4],
472	            [x, y],
473	          ],
474	          diamondOptions,
475	        ),
476	      ];
477	    }
478	    case "cardinality_one":
479	      return generateArrowheadCardinalityOne(
480	        generator,
481	        getArrowheadPoints(element, shape, position, arrowhead),
482	        getArrowheadLineOptions(element, options),
483	      );
484	    case "cardinality_many":
485	      return generateArrowheadLinesToTip(
486	        generator,
487	        getArrowheadPoints(element, shape, position, arrowhead),
488	        getArrowheadLineOptions(element, options),
489	      );
490	    case "cardinality_one_or_many": {
491	      const lineOptions = getArrowheadLineOptions(element, options);
492	
493	      return [
494	        ...generateArrowheadLinesToTip(
495	          generator,
496	          getArrowheadPoints(element, shape, position, "cardinality_many"),
497	          lineOptions,
498	        ),
499	        ...generateArrowheadCardinalityOne(
500	          generator,
501	          getArrowheadPoints(
502	            element,
503	            shape,
504	            position,
505	            "cardinality_one",
506	            cardinalityOneOrManyOffset,
507	          ),
508	          lineOptions,
509	        ),
510	      ];
511	    }
512	    case "cardinality_exactly_one": {
513	      const lineOptions = getArrowheadLineOptions(element, options);
514	
515	      return [
516	        ...generateArrowheadCardinalityOne(
517	          generator,
518	          getArrowheadPoints(element, shape, position, "cardinality_one", -0.5),
519	          lineOptions,
520	        ),
521	        ...generateArrowheadCardinalityOne(
522	          generator,
523	          getArrowheadPoints(element, shape, position, "cardinality_one"),
524	          lineOptions,
525	        ),
526	      ];
527	    }
528	    case "cardinality_zero_or_one": {
529	      const lineOptions = getArrowheadLineOptions(element, options);
530	
531	      return [
532	        ...generateArrowheadOutlineCircle(
533	          generator,
534	          options,
535	          strokeColor,
536	          getArrowheadPoints(element, shape, position, "circle_outline", 1.5),
537	          backgroundFillColor,
538	          cardinalityZeroCircleScale,
539	        ),
540	        ...generateArrowheadCardinalityOne(
541	          generator,
542	          getArrowheadPoints(element, shape, position, "cardinality_one", -0.5),
543	          lineOptions,
544	        ),
545	      ];
546	    }
547	    case "cardinality_zero_or_many": {
548	      const lineOptions = getArrowheadLineOptions(element, options);
549	
550	      return [
551	        ...generateArrowheadLinesToTip(
552	          generator,
553	          getArrowheadPoints(element, shape, position, "cardinality_many"),
554	          lineOptions,
555	        ),
556	        ...generateArrowheadOutlineCircle(
557	          generator,
558	          options,
559	          strokeColor,
560	          getArrowheadPoints(element, shape, position, "circle_outline", 1.5),
561	          backgroundFillColor,
562	          cardinalityZeroCircleScale,
563	        ),
564	      ];
565	    }
566	    case "bar":
567	    case "arrow":
568	    default: {
569	      return generateArrowheadLinesToTip(
570	        generator,
571	        getArrowheadPoints(element, shape, position, arrowhead),
572	        getArrowheadLineOptions(element, options),
573	      );
574	    }
575	  }
576	};
577	
578	export const generateLinearCollisionShape = (
579	  element: ExcalidrawLinearElement | ExcalidrawFreeDrawElement,
580	  elementsMap: ElementsMap,
581	): {
582	  op: string;
583	  data: number[];
584	}[] => {
585	  const generator = new RoughGenerator();
586	  const options: Options = {
587	    seed: element.seed,
588	    disableMultiStroke: true,
589	    disableMultiStrokeFill: true,
590	    roughness: 0,
591	    preserveVertices: true,
592	  };
593	  const center = elementCenterPoint(element, elementsMap);
594	
595	  switch (element.type) {
596	    case "line":
597	    case "arrow": {
598	      // points array can be empty in the beginning, so it is important to add
599	      // initial position to it
600	      const points = element.points.length
601	        ? element.points
602	        : [pointFrom<LocalPoint>(0, 0)];
603	
604	      if (isElbowArrow(element)) {
605	        return generator.path(generateElbowArrowShape(points, 16), options)
606	          .sets[0].ops;
607	      } else if (!element.roundness) {
608	        return points.map((point, idx) => {
609	          const p = pointRotateRads(
610	            pointFrom<GlobalPoint>(element.x + point[0], element.y + point[1]),
611	            center,
612	            element.angle,
613	          );
614	
615	          return {
616	            op: idx === 0 ? "move" : "lineTo",
617	            data: pointFrom<LocalPoint>(p[0] - element.x, p[1] - element.y),
618	          };
619	        });
620	      }
621	
622	      return generator
623	        .curve(points as unknown as RoughPoint[], options)
624	        .sets[0].ops.slice(0, element.points.length)
625	        .map((op, i) => {
626	          if (i === 0) {
627	            const p = pointRotateRads<GlobalPoint>(
628	              pointFrom<GlobalPoint>(
629	                element.x + op.data[0],
630	                element.y + op.data[1],
631	              ),
632	              center,
633	              element.angle,
634	            );
635	
636	            return {
637	              op: "move",
638	              data: pointFrom<LocalPoint>(p[0] - element.x, p[1] - element.y),
639	            };
640	          }
641	
642	          return {
643	            op: "bcurveTo",
644	            data: [
645	              pointRotateRads(
646	                pointFrom<GlobalPoint>(
647	                  element.x + op.data[0],
648	                  element.y + op.data[1],
649	                ),
650	                center,
651	                element.angle,
652	              ),
653	              pointRotateRads(
654	                pointFrom<GlobalPoint>(
655	                  element.x + op.data[2],
656	                  element.y + op.data[3],
657	                ),
658	                center,
659	                element.angle,
660	              ),
661	              pointRotateRads(
662	                pointFrom<GlobalPoint>(
663	                  element.x + op.data[4],
664	                  element.y + op.data[5],
665	                ),
666	                center,
667	                element.angle,
668	              ),
669	            ]
670	              .map((p) =>
671	                pointFrom<LocalPoint>(p[0] - element.x, p[1] - element.y),
672	              )
673	              .flat(),
674	          };
675	        });
676	    }
677	    case "freedraw": {
678	      if (element.points.length < 2) {
679	        return [];
680	      }
681	
682	      const simplifiedPoints = simplify(
683	        element.points as Mutable<LocalPoint[]>,
684	        0.75,
685	      );
686	
687	      return generator
688	        .curve(simplifiedPoints as [number, number][], options)
689	        .sets[0].ops.slice(0, element.points.length)
690	        .map((op, i) => {
691	          if (i === 0) {
692	            const p = pointRotateRads<GlobalPoint>(
693	              pointFrom<GlobalPoint>(
694	                element.x + op.data[0],
695	                element.y + op.data[1],
696	              ),
697	              center,
698	              element.angle,
699	            );
700	
701	            return {
702	              op: "move",
703	              data: pointFrom<LocalPoint>(p[0] - element.x, p[1] - element.y),
704	            };
705	          }
706	
707	          return {
708	            op: "bcurveTo",
709	            data: [
710	              pointRotateRads(
711	                pointFrom<GlobalPoint>(
712	                  element.x + op.data[0],
713	                  element.y + op.data[1],
714	                ),
715	                center,
716	                element.angle,
717	              ),
718	              pointRotateRads(
719	                pointFrom<GlobalPoint>(
720	                  element.x + op.data[2],
721	                  element.y + op.data[3],
722	                ),
723	                center,
724	                element.angle,
725	              ),
726	              pointRotateRads(
727	                pointFrom<GlobalPoint>(
728	                  element.x + op.data[4],
729	                  element.y + op.data[5],
730	                ),
731	                center,
732	                element.angle,
733	              ),
734	            ]
735	              .map((p) =>
736	                pointFrom<LocalPoint>(p[0] - element.x, p[1] - element.y),
737	              )
738	              .flat(),
739	          };
740	        });
741	    }
742	  }
743	};
744	
745	/**
746	 * Generates the roughjs shape for given element.
747	 *
748	 * Low-level. Use `ShapeCache.generateElementShape` instead.
749	 *
750	 * @private
751	 */
752	const _generateElementShape = (
753	  element: Exclude<ExcalidrawElement, ExcalidrawSelectionElement>,
754	  generator: RoughGenerator,
755	  {
756	    isExporting,
757	    canvasBackgroundColor,
758	    embedsValidationStatus,
759	    theme,
760	  }: {
761	    isExporting: boolean;
762	    canvasBackgroundColor: string;
763	    embedsValidationStatus: EmbedsValidationStatus | null;
764	    theme?: AppState["theme"];
765	  },
766	): ElementShape => {
767	  const isDarkMode = theme === THEME.DARK;
768	  switch (element.type) {
769	    case "rectangle":
770	    case "iframe":
771	    case "embeddable": {
772	      let shape: ElementShapes[typeof element.type];
773	      // this is for rendering the stroke/bg of the embeddable, especially
774	      // when the src url is not set
775	
776	      if (element.roundness) {
777	        const w = element.width;
778	        const h = element.height;
779	        const r = getCornerRadius(Math.min(w, h), element);
780	        shape = generator.path(
781	          `M ${r} 0 L ${w - r} 0 Q ${w} 0, ${w} ${r} L ${w} ${
782	            h - r
783	          } Q ${w} ${h}, ${w - r} ${h} L ${r} ${h} Q 0 ${h}, 0 ${
784	            h - r
785	          } L 0 ${r} Q 0 0, ${r} 0`,
786	          generateRoughOptions(
787	            modifyIframeLikeForRoughOptions(
788	              element,
789	              isExporting,
790	              embedsValidationStatus,
791	            ),
792	            true,
793	            isDarkMode,
794	          ),
795	        );
796	      } else {
797	        shape = generator.rectangle(
798	          0,
799	          0,
800	          element.width,
801	          element.height,
802	          generateRoughOptions(
803	            modifyIframeLikeForRoughOptions(
804	              element,
805	              isExporting,
806	              embedsValidationStatus,
807	            ),
808	            false,
809	            isDarkMode,
810	          ),
811	        );
812	      }
813	      return shape;
814	    }
815	    case "diamond": {
816	      let shape: ElementShapes[typeof element.type];
817	
818	      const [topX, topY, rightX, rightY, bottomX, bottomY, leftX, leftY] =
819	        getDiamondPoints(element);
820	      if (element.roundness) {
821	        const verticalRadius = getCornerRadius(Math.abs(topX - leftX), element);
822	
823	        const horizontalRadius = getCornerRadius(
824	          Math.abs(rightY - topY),
825	          element,
826	        );
827	
828	        shape = generator.path(
829	          `M ${topX + verticalRadius} ${topY + horizontalRadius} L ${
830	            rightX - verticalRadius
831	          } ${rightY - horizontalRadius}
832	            C ${rightX} ${rightY}, ${rightX} ${rightY}, ${
833	            rightX - verticalRadius
834	          } ${rightY + horizontalRadius}
835	            L ${bottomX + verticalRadius} ${bottomY - horizontalRadius}
836	            C ${bottomX} ${bottomY}, ${bottomX} ${bottomY}, ${
837	            bottomX - verticalRadius
838	          } ${bottomY - horizontalRadius}
839	            L ${leftX + verticalRadius} ${leftY + horizontalRadius}
840	            C ${leftX} ${leftY}, ${leftX} ${leftY}, ${leftX + verticalRadius} ${
841	            leftY - horizontalRadius
842	          }
843	            L ${topX - verticalRadius} ${topY + horizontalRadius}
844	            C ${topX} ${topY}, ${topX} ${topY}, ${topX + verticalRadius} ${
845	            topY + horizontalRadius
846	          }`,
847	          generateRoughOptions(element, true, isDarkMode),
848	        );
849	      } else {
850	        shape = generator.polygon(
851	          [
852	            [topX, topY],
853	            [rightX, rightY],
854	            [bottomX, bottomY],
855	            [leftX, leftY],
856	          ],
857	          generateRoughOptions(element, false, isDarkMode),
858	        );
859	      }
860	      return shape;
861	    }
862	    case "ellipse": {
863	      const shape: ElementShapes[typeof element.type] = generator.ellipse(
864	        element.width / 2,
865	        element.height / 2,
866	        element.width,
867	        element.height,
868	        generateRoughOptions(element, false, isDarkMode),
869	      );
870	      return shape;
871	    }
872	    case "line":
873	    case "arrow": {
874	      let shape: ElementShapes[typeof element.type];
875	      const options = generateRoughOptions(element, false, isDarkMode);
876	
877	      // points array can be empty in the beginning, so it is important to add
878	      // initial position to it
879	      const points = element.points.length
880	        ? element.points
881	        : [pointFrom<LocalPoint>(0, 0)];
882	
883	      if (isElbowArrow(element)) {
884	        // NOTE (mtolmacs): Temporary fix for extremely big arrow shapes
885	        if (
886	          !points.every(
887	            (point) => Math.abs(point[0]) <= 1e6 && Math.abs(point[1]) <= 1e6,
888	          )
889	        ) {
890	          console.error(
891	            `Elbow arrow with extreme point positions detected. Arrow not rendered.`,
892	            element.id,
893	            JSON.stringify(points),
894	          );
895	          shape = [];
896	        } else {
897	          shape = [
898	            generator.path(
899	              generateElbowArrowShape(points, 16),
900	              generateRoughOptions(element, true, isDarkMode),
901	            ),
902	          ];
903	        }
904	      } else if (!element.roundness) {
905	        // curve is always the first element
906	        // this simplifies finding the curve for an element
907	        if (options.fill) {
908	          shape = [
909	            generator.polygon(points as unknown as RoughPoint[], options),
910	          ];
911	        } else {
912	          shape = [
913	            generator.linearPath(points as unknown as RoughPoint[], options),
914	          ];
915	        }
916	      } else {
917	        shape = [generator.curve(points as unknown as RoughPoint[], options)];
918	      }
919	
920	      // add lines only in arrow
921	      if (element.type === "arrow") {
922	        const { startArrowhead = null, endArrowhead = "arrow" } = element;
923	
924	        if (startArrowhead !== null) {
925	          const shapes = getArrowheadShapes(
926	            element,
927	            shape,
928	            "start",
929	            startArrowhead,
930	            generator,
931	            options,
932	            canvasBackgroundColor,
933	            isDarkMode,
934	          );
935	          shape.push(...shapes);
936	        }
937	
938	        if (endArrowhead !== null) {
939	          if (endArrowhead === undefined) {
940	            // Hey, we have an old arrow here!
941	          }
942	
943	          const shapes = getArrowheadShapes(
944	            element,
945	            shape,
946	            "end",
947	            endArrowhead,
948	            generator,
949	            options,
950	            canvasBackgroundColor,
951	            isDarkMode,
952	          );
953	          shape.push(...shapes);
954	        }
955	      }
956	      return shape;
957	    }
958	    case "freedraw": {
959	      // oredered in terms of z-index [background, stroke]
960	      const shapes: ElementShapes[typeof element.type] = [];
961	
962	      // (1) background fill (rc shape), optional
963	      if (isPathALoop(element.points)) {
964	        // generate rough polygon to fill freedraw shape
965	        const simplifiedPoints = simplify(
966	          element.points as Mutable<LocalPoint[]>,
967	          0.75,
968	        );
969	        shapes.push(
970	          generator.curve(simplifiedPoints as [number, number][], {
971	            ...generateRoughOptions(element, false, isDarkMode),
972	            stroke: "none",
973	          }),
974	        );
975	      }
976	
977	      // (2) stroke
978	      shapes.push(getFreeDrawSvgPath(element));
979	
980	      return shapes;
981	    }
982	    case "frame":
983	    case "magicframe":
984	    case "text":
985	    case "image": {
986	      const shape: ElementShapes[typeof element.type] = null;
987	      // we return (and cache) `null` to make sure we don't regenerate
988	      // `element.canvas` on rerenders
989	      return shape;
990	    }
991	    default: {
992	      assertNever(
993	        element,
994	        `generateElementShape(): Unimplemented type ${(element as any)?.type}`,
995	      );
996	      return null;
997	    }
998	  }
999	};
1000	
1001	const generateElbowArrowShape = (
1002	  points: readonly LocalPoint[],
1003	  radius: number,
1004	) => {
1005	  const subpoints = [] as [number, number][];
1006	  for (let i = 1; i < points.length - 1; i += 1) {
1007	    const prev = points[i - 1];
1008	    const next = points[i + 1];
1009	    const point = points[i];
1010	    const prevIsHorizontal = headingForPointIsHorizontal(point, prev);
1011	    const nextIsHorizontal = headingForPointIsHorizontal(next, point);
1012	    const corner = Math.min(
1013	      radius,
1014	      pointDistance(points[i], next) / 2,
1015	      pointDistance(points[i], prev) / 2,
1016	    );
1017	
1018	    if (prevIsHorizontal) {
1019	      if (prev[0] < point[0]) {
1020	        // LEFT
1021	        subpoints.push([points[i][0] - corner, points[i][1]]);
1022	      } else {
1023	        // RIGHT
1024	        subpoints.push([points[i][0] + corner, points[i][1]]);
1025	      }
1026	    } else if (prev[1] < point[1]) {
1027	      // UP
1028	      subpoints.push([points[i][0], points[i][1] - corner]);
1029	    } else {
1030	      subpoints.push([points[i][0], points[i][1] + corner]);
1031	    }
1032	
1033	    subpoints.push(points[i] as [number, number]);
1034	
1035	    if (nextIsHorizontal) {
1036	      if (next[0] < point[0]) {
1037	        // LEFT
1038	        subpoints.push([points[i][0] - corner, points[i][1]]);
1039	      } else {
1040	        // RIGHT
1041	        subpoints.push([points[i][0] + corner, points[i][1]]);
1042	      }
1043	    } else if (next[1] < point[1]) {
1044	      // UP
1045	      subpoints.push([points[i][0], points[i][1] - corner]);
1046	    } else {
1047	      // DOWN
1048	      subpoints.push([points[i][0], points[i][1] + corner]);
1049	    }
1050	  }
1051	
1052	  const d = [`M ${points[0][0]} ${points[0][1]}`];
1053	  for (let i = 0; i < subpoints.length; i += 3) {
1054	    d.push(`L ${subpoints[i][0]} ${subpoints[i][1]}`);
1055	    d.push(
1056	      `Q ${subpoints[i + 1][0]} ${subpoints[i + 1][1]}, ${
1057	        subpoints[i + 2][0]
1058	      } ${subpoints[i + 2][1]}`,
1059	    );
1060	  }
1061	  d.push(`L ${points[points.length - 1][0]} ${points[points.length - 1][1]}`);
1062	
1063	  return d.join(" ");
1064	};
1065	
1066	/**
1067	 * get the pure geometric shape of an excalidraw elementw
1068	 * which is then used for hit detection
1069	 */
1070	export const getElementShape = <Point extends GlobalPoint | LocalPoint>(
1071	  element: ExcalidrawElement,
1072	  elementsMap: ElementsMap,
1073	): GeometricShape<Point> => {
1074	  switch (element.type) {
1075	    case "rectangle":
1076	    case "diamond":
1077	    case "frame":
1078	    case "magicframe":
1079	    case "embeddable":
1080	    case "image":
1081	    case "iframe":
1082	    case "text":
1083	    case "selection":
1084	      return getPolygonShape(element);
1085	    case "arrow":
1086	    case "line": {
1087	      const roughShape = ShapeCache.generateElementShape(element, null)[0];
1088	      const [, , , , cx, cy] = getElementAbsoluteCoords(element, elementsMap);
1089	
1090	      return shouldTestInside(element)
1091	        ? getClosedCurveShape<Point>(
1092	            element,
1093	            roughShape,
1094	            pointFrom<Point>(element.x, element.y),
1095	            element.angle,
1096	            pointFrom(cx, cy),
1097	          )
1098	        : getCurveShape<Point>(
1099	            roughShape,
1100	            pointFrom<Point>(element.x, element.y),
1101	            element.angle,
1102	            pointFrom(cx, cy),
1103	          );
1104	    }
1105	
1106	    case "ellipse":
1107	      return getEllipseShape(element);
1108	
1109	    case "freedraw": {
1110	      const [, , , , cx, cy] = getElementAbsoluteCoords(element, elementsMap);
1111	      return getFreedrawShape(
1112	        element,
1113	        pointFrom(cx, cy),
1114	        shouldTestInside(element),
1115	      );
1116	    }
1117	  }
1118	};
1119	
1120	export const toggleLinePolygonState = (
1121	  element: ExcalidrawLineElement,
1122	  nextPolygonState: boolean,
1123	): {
1124	  polygon: ExcalidrawLineElement["polygon"];
1125	  points: ExcalidrawLineElement["points"];
1126	} | null => {
1127	  const updatedPoints = [...element.points];
1128	
1129	  if (nextPolygonState) {
1130	    if (!canBecomePolygon(element.points)) {
1131	      return null;
1132	    }
1133	
1134	    const firstPoint = updatedPoints[0];
1135	    const lastPoint = updatedPoints[updatedPoints.length - 1];
1136	
1137	    const distance = Math.hypot(
1138	      firstPoint[0] - lastPoint[0],
1139	      firstPoint[1] - lastPoint[1],
1140	    );
1141	
1142	    if (
1143	      distance > LINE_POLYGON_POINT_MERGE_DISTANCE ||
1144	      updatedPoints.length < 4
1145	    ) {
1146	      updatedPoints.push(pointFrom(firstPoint[0], firstPoint[1]));
1147	    } else {
1148	      updatedPoints[updatedPoints.length - 1] = pointFrom(
1149	        firstPoint[0],
1150	        firstPoint[1],
1151	      );
1152	    }
1153	  }
1154	
1155	  // TODO: satisfies ElementUpdate<ExcalidrawLineElement>
1156	  const ret = {
1157	    polygon: nextPolygonState,
1158	    points: updatedPoints,
1159	  };
1160	
1161	  return ret;
1162	};
1163	
1164	// -----------------------------------------------------------------------------
1165	//                         freedraw shape helper
1166	// -----------------------------------------------------------------------------
1167	
1168	// NOTE not cached (-> for SVG export)
1169	const getFreeDrawSvgPath = (element: ExcalidrawFreeDrawElement) => {
1170	  return getSvgPathFromStroke(
1171	    getFreedrawOutlinePoints(element),
1172	  ) as SVGPathString;
1173	};
1174	
1175	/**
1176	 * Freedraw stroke geometry tuning constants.
1177	 *
1178	 * These factors are not derived analytically — they were tuned empirically by
1179	 * visually comparing rendered strokes until they matched the desired feel.
1180	 * Treat them as magic numbers backed by visual verification.
1181	 */
1182	const VARIABLE_WIDTH_FREEDRAW = {
1183	  /** Stroke size relative to `strokeWidth` for pressure-sensitive strokes. */
1184	  SIZE_FACTOR: 4.25,
1185	  THINNING: 0.6,
1186	  SMOOTHING: 0.5,
1187	} as const;
1188	
1189	const CONSTANT_WIDTH_FREEDRAW = {
1190	  /** Stroke size relative to `strokeWidth` for uniform (laser) strokes. */
1191	  SIZE_FACTOR: 1.4,
1192	} as const;
1193	
1194	const getFreedrawStreamline = (element: ExcalidrawFreeDrawElement) =>
1195	  element.strokeOptions?.streamline ?? DEFAULT_STROKE_STREAMLINE;
1196	
1197	/**
1198	 * Pressure-sensitive (variable width) freedraw outline, rendered with
1199	 * perfect-freehand. This is the original Excalidraw freedraw look.
1200	 */
1201	const getVariableWidthFreedrawOutline = (
1202	  element: ExcalidrawFreeDrawElement,
1203	): [number, number][] => {
1204	  // If input points are empty (should they ever be?) return a dot
1205	  const inputPoints = element.simulatePressure
1206	    ? element.points
1207	    : element.points.length
1208	    ? element.points.map(
1209	        ([x, y], i) => [x, y, element.pressures[i]] as [number, number, number],
1210	      )
1211	    : [[0, 0, 0.5]];
1212	
1213	  return getStroke(inputPoints as number[][], {
1214	    simulatePressure: element.simulatePressure,
1215	    size: element.strokeWidth * VARIABLE_WIDTH_FREEDRAW.SIZE_FACTOR,
1216	    thinning: VARIABLE_WIDTH_FREEDRAW.THINNING,
1217	    smoothing: VARIABLE_WIDTH_FREEDRAW.SMOOTHING,
1218	    streamline: getFreedrawStreamline(element),
1219	    easing: (t) => Math.sin((t * Math.PI) / 2), // https://easings.net/#easeOutSine
1220	    last: true,
1221	  }) as [number, number][];
1222	};
1223	
1224	const createLaserPointer = (element: ExcalidrawFreeDrawElement) =>
1225	  new LaserPointer({
1226	    size: element.strokeWidth * CONSTANT_WIDTH_FREEDRAW.SIZE_FACTOR,
1227	    streamline: getFreedrawStreamline(element),
1228	    simplify: 0,
1229	    sizeMapping: (details) => Math.max(0.1, details.pressure),
1230	  });
1231	
1232	/**
1233	 * Uniform (constant width) freedraw outline, rendered with the laser-pointer
1234	 * geometry. Pressure is pinned to 1 so the stroke keeps a constant width.
1235	 */
1236	const getConstantWidthFreedrawOutline = (
1237	  element: ExcalidrawFreeDrawElement,
1238	): [number, number][] => {
1239	  const laserPointer = createLaserPointer(element);
1240	  element.points.map(([x, y]) => laserPointer.addPoint([x, y, 1]));
1241	
1242	  return laserPointer
1243	    .getStrokeOutline()
1244	    .map(([x, y]) => [x, y] as [number, number]);
1245	};
1246	
1247	export const getFreedrawOutlinePoints = (
1248	  element: ExcalidrawFreeDrawElement,
1249	): [number, number][] => {
1250	  // Unknown/absent variability falls back to the original variable rendering.
1251	  return element.strokeOptions?.variability === "constant"
1252	    ? getConstantWidthFreedrawOutline(element)
1253	    : getVariableWidthFreedrawOutline(element);
1254	};
1255	
1256	/**
1257	 * The streamline-smoothed centerline the freedraw stroke is rendered
1258	 * around, in element-local coordinates. Boundary-sensitive consumers (e.g.
1259	 * bucket fill) should use this instead of `element.points`: raw input
1260	 * points can sit 20px+ apart and the rendered stroke is smoothed between
1261	 * them, so raw chords visibly deviate from what's on screen.
1262	 *
1263	 * Constant-width ("laser geometry") strokes technically smooth via
1264	 * `LaserPointer` instead; the perfect-freehand centerline with the same
1265	 * `streamline` is a close approximation the stroke width hides.
1266	 */
1267	export const getFreedrawStrokeCenterPoints = (
1268	  element: ExcalidrawFreeDrawElement,
1269	): [number, number][] =>
1270	  getStrokePoints(element.points as unknown as number[][], {
1271	    size: element.strokeWidth * VARIABLE_WIDTH_FREEDRAW.SIZE_FACTOR,
1272	    streamline: getFreedrawStreamline(element),
1273	    last: true,
1274	  }).map((strokePoint) => strokePoint.point as [number, number]);
1275	
1276	const med = (A: number[], B: number[]) => {
1277	  return [(A[0] + B[0]) / 2, (A[1] + B[1]) / 2];
1278	};
1279	
1280	// Trim SVG path data so number are each two decimal points. This
1281	// improves SVG exports, and prevents rendering errors on points
1282	// with long decimals.
1283	const TO_FIXED_PRECISION = /(\s?[A-Z]?,?-?[0-9]*\.[0-9]{0,2})(([0-9]|e|-)*)/g;
1284	
1285	const getSvgPathFromStroke = (points: number[][]): string => {
1286	  if (!points.length) {
1287	    return "";
1288	  }
1289	
1290	  const max = points.length - 1;
1291	
1292	  return points
1293	    .reduce(
1294	      (acc, point, i, arr) => {
1295	        if (i === max) {
1296	          acc.push(point, med(point, arr[0]), "L", arr[0], "Z");
1297	        } else {
1298	          acc.push(point, med(point, arr[i + 1]));
1299	        }
1300	        return acc;
1301	      },
1302	      ["M", points[0], "Q"],
1303	    )
1304	    .join(" ")
1305	    .replace(TO_FIXED_PRECISION, "$1");
1306	};
1307	
1308	// -----------------------------------------------------------------------------
1309	
```

> Now let's look at renderElement.ts (dispatch by type), Scene.ts (element storage/versioning), and App.tsx's scheduling calls, plus throttleRAF utility.

## 11. `Bash` (sub-agent)

```json
{
 "command": "cd \"C:\\work\\excalidraw\" && grep -n \"^export const renderElement\\|^const renderElementBase\\|switch (element.type)\\|elementWithCanvasCache\\|export class.*Cache\" packages/element/src/renderElement.ts | head -50",
 "description": "Find renderElement dispatch and cache"
}
```
**result of 11**
```
94:  switch (element.type) {
324:  switch (element.type) {
534:export const elementWithCanvasCache = new WeakMap<
550:  const prevElementWithCanvas = elementWithCanvasCache.get(element);
579:    elementWithCanvasCache.set(element, elementWithCanvas);
810:export const renderElement = (
832:  switch (element.type) {
```

## 12. `Bash` (sub-agent)

```json
{
 "command": "cd \"C:\\work\\excalidraw\" && grep -n \"class Scene\\|versionNonce\\|getVersion\\|sceneNonce\\|elements\\s*=\\|private elements\\|getNonDeletedElements\\|getElement\\b\\|mapElementToScene\\|triggerUpdate\\|informMutation\" packages/element/src/Scene.ts | head -60",
 "description": "Find Scene class key members"
}
```
**result of 12**
```
50:const getNonDeletedElements = <T extends ExcalidrawElement>(
108:export class Scene {
121:  private elements: readonly OrderedExcalidrawElement[] = [];
125:  private elementsMap = toBrandedType<SceneElementsMap>(new Map());
141:  private sceneNonce: number | undefined;
144:    return this.sceneNonce;
147:  getNonDeletedElementsMap() {
159:  getNonDeletedElements() {
193:    const elements = opts?.elements || this.nonDeletedElements;
195:      this.selectedElementsCache.elements === elements &&
202:    } else if (opts?.elements == null) {
215:    if (opts?.elements == null) {
217:      this.selectedElementsCache.elements = this.nonDeletedElements;
228:  getElement<T extends ExcalidrawElement>(id: T["id"]): T | null {
235:    const element = this.getElement(id);
285:    this.elements = syncInvalidIndices(_nextElements);
293:    const nonDeletedElements = getNonDeletedElements(this.elements);
298:    this.nonDeletedFramesLikes = getNonDeletedElements(this.frames).elements;
300:    this.triggerUpdate();
303:  triggerUpdate() {
304:    this.sceneNonce = randomInteger();
327:    this.elements = [];
333:    this.selectedElementsCache.elements = null;
392:      return this.getElement(element.containerId) || null;
398:    const elementsMap = this.getNonDeletedElementsMap();
415:      informMutation: boolean;
420:      informMutation: true,
424:    const elementsMap = this.getNonDeletedElementsMap();
439:      options.informMutation
441:      this.triggerUpdate();
```

## 13. `Read` (sub-agent)

```json
{
 "file_path": "C:\\work\\excalidraw\\packages\\element\\src\\renderElement.ts",
 "offset": 530,
 "limit": 320
}
```
**result of 13**
```
530	    }
531	  }
532	};
533	
534	export const elementWithCanvasCache = new WeakMap<
535	  ExcalidrawElement,
536	  ExcalidrawElementWithCanvas
537	>();
538	
539	const generateElementWithCanvas = (
540	  element: NonDeletedExcalidrawElement,
541	  elementsMap: NonDeletedSceneElementsMap,
542	  renderConfig: StaticCanvasRenderConfig,
543	  appState: StaticCanvasAppState | InteractiveCanvasAppState,
544	) => {
545	  const zoom: Zoom = renderConfig
546	    ? appState.zoom
547	    : {
548	        value: 1 as NormalizedZoomValue,
549	      };
550	  const prevElementWithCanvas = elementWithCanvasCache.get(element);
551	  const shouldRegenerateBecauseZoom =
552	    prevElementWithCanvas &&
553	    prevElementWithCanvas.zoomValue !== zoom.value &&
554	    !appState?.shouldCacheIgnoreZoom;
555	  const imageCrop = isImageElement(element) ? element.crop : null;
556	
557	  const containingFrameOpacity =
558	    getContainingFrame(element, elementsMap)?.opacity || 100;
559	
560	  if (
561	    !prevElementWithCanvas ||
562	    shouldRegenerateBecauseZoom ||
563	    prevElementWithCanvas.theme !== appState.theme ||
564	    prevElementWithCanvas.imageCrop !== imageCrop ||
565	    prevElementWithCanvas.containingFrameOpacity !== containingFrameOpacity
566	  ) {
567	    const elementWithCanvas = generateElementCanvas(
568	      element,
569	      elementsMap,
570	      zoom,
571	      renderConfig,
572	      appState,
573	    );
574	
575	    if (!elementWithCanvas) {
576	      return null;
577	    }
578	
579	    elementWithCanvasCache.set(element, elementWithCanvas);
580	
581	    return elementWithCanvas;
582	  }
583	  return prevElementWithCanvas;
584	};
585	
586	/**
587	 * Whether an element's cached bitmap may be laid on the device-pixel grid:
588	 * unrotated or at a right angle, and not during a zoom gesture. The cached
589	 * path disables smoothing for exactly these — a nearest-neighbor 1:1 blit is
590	 * a pixel-exact copy, and rounding its origin keeps it off the half-pixel
591	 * boundary where it tears — and every eligible blit is snapped. It is
592	 * eligibility, not a guarantee of a 1:1 copy: freedraw is blitted with
593	 * smoothing on, and a size-capped cache is rescaled; snapping is harmless
594	 * for both.
595	 *
596	 * Not during a zoom gesture: the bitmaps stay at the old scale and are
597	 * resampled, and blurry shapes look better on low resolution (while still
598	 * zooming in) than sharp ones; snapping would only make elements twitch.
599	 * Right angles qualify because smoothing can be off there without aliasing
600	 * (for other angles it is terrible on Chromium); the right-angle test
601	 * tolerates float arithmetic.
602	 */
603	const canSnapElement = (
604	  element: ExcalidrawElement,
605	  appState: StaticCanvasAppState | InteractiveCanvasAppState,
606	) =>
607	  !appState?.shouldCacheIgnoreZoom &&
608	  (!element.angle || isRightAngleRads(element.angle));
609	
610	/**
611	 * Breaks a `Math.round` tie at exactly half a device pixel the same way
612	 * every frame. A label's offset from its container lands on one routinely
613	 * (an odd scene offset at 150%), and the float noise of a fractional drag
614	 * would otherwise flip it between the two neighbors.
615	 */
616	const SNAP_TIE_BIAS = 1e-6;
617	
618	const drawElementFromCanvas = (
619	  elementWithCanvas: ExcalidrawElementWithCanvas,
620	  context: CanvasRenderingContext2D,
621	  renderConfig: StaticCanvasRenderConfig,
622	  appState: StaticCanvasAppState | InteractiveCanvasAppState,
623	  allElementsMap: NonDeletedSceneElementsMap,
624	) => {
625	  const element = elementWithCanvas.element;
626	  // the ratio the cached bitmap was generated with (`generateElementCanvas`);
627	  // the blit's size math needs the same one, so it is not the owner window's
628	  const devicePixelRatio = window.devicePixelRatio;
629	  const padding = getCanvasPadding(element);
630	  const [x1, y1, x2, y2] = getElementAbsoluteCoords(element, allElementsMap);
631	  const cx = ((x1 + x2) / 2 + appState.scrollX) * devicePixelRatio;
632	  const cy = ((y1 + y2) / 2 + appState.scrollY) * devicePixelRatio;
633	
634	  context.save();
635	  context.scale(1 / devicePixelRatio, 1 / devicePixelRatio);
636	
637	  const boundTextElement = getBoundTextElement(element, allElementsMap);
638	
639	  if (isArrowElement(element) && boundTextElement) {
640	    // punch the label "hole" by clipping the arrow's blit out of the label
641	    // rect (even-odd) instead of baking a rotated arrow copy with a cleared
642	    // hole into a separate (`maxDim`-squared!) canvas. The hole stays
643	    // axis-aligned in scene space while the blit below rotates.
644	    const [, , , , boundTextCx, boundTextCy] = getElementAbsoluteCoords(
645	      boundTextElement,
646	      allElementsMap,
647	    );
648	    // generously covers the arrow's blit at any rotation
649	    const outerHalf =
650	      Math.max(distance(x1, x2), distance(y1, y2)) * devicePixelRatio +
651	      padding * 10;
652	    context.beginPath();
653	    context.rect(cx - outerHalf, cy - outerHalf, outerHalf * 2, outerHalf * 2);
654	    context.rect(
655	      (boundTextCx -
656	        boundTextElement.width / 2 -
657	        BOUND_TEXT_PADDING +
658	        appState.scrollX) *
659	        devicePixelRatio,
660	      (boundTextCy -
661	        boundTextElement.height / 2 -
662	        BOUND_TEXT_PADDING +
663	        appState.scrollY) *
664	        devicePixelRatio,
665	      (boundTextElement.width + BOUND_TEXT_PADDING * 2) * devicePixelRatio,
666	      (boundTextElement.height + BOUND_TEXT_PADDING * 2) * devicePixelRatio,
667	    );
668	    context.clip("evenodd");
669	  }
670	
671	  // we translate context to element center so that rotation and scale
672	  // originates from the element center
673	  context.translate(cx, cy);
674	
675	  context.rotate(element.angle);
676	
677	  if (
678	    "scale" in elementWithCanvas.element &&
679	    !isPendingImageElement(element, renderConfig)
680	  ) {
681	    context.scale(
682	      elementWithCanvas.element.scale[0],
683	      elementWithCanvas.element.scale[1],
684	    );
685	  }
686	
687	  // revert afterwards we don't have account for it during drawing
688	  context.translate(-cx, -cy);
689	
690	  // the blit origin, in the space the context is in here (scaled by
691	  // canvas scale × zoom ÷ devicePixelRatio)
692	  let drawX = (x1 + appState.scrollX) * devicePixelRatio - padding;
693	  let drawY = (y1 + appState.scrollY) * devicePixelRatio - padding;
694	
695	  const transform = context.getTransform();
696	
697	  if (canSnapElement(element, appState)) {
698	    // blit the cached bitmap on whole device pixels. Nearest-neighbor at a
699	    // fractional offset is a pixel-exact copy shifted to the nearest pixel
700	    // — except at an exact half pixel, where a GPU-accelerated canvas
701	    // decides the rounding per scanline by float precision and a few rows
702	    // sample the neighboring row: doubled or broken strokes, varying with
703	    // scroll and position. A centered label lands on a half pixel
704	    // routinely.
705	    //
706	    // Done by moving the transform's origin onto the rounded device
707	    // position of the blit and drawing at (0, 0): the rotation, mirroring
708	    // and scale stay in `a`–`d` (a right angle keeps its scale in `b`/`c`),
709	    // and the origin is an exact integer even in the canvas's float32
710	    // matrix. Rounding `drawX` itself only lands on device pixels at 100%
711	    // zoom.
712	    const { a, b, c, d, e, f } = transform;
713	    const container = isTextElement(element)
714	      ? getContainerElement(element, allElementsMap)
715	      : null;
716	    // A bound label shares its unrotated container's anchor. Other bitmaps
717	    // anchor to themselves, with a zero relative offset.
718	    const anchor = container && !container.angle ? container : element;
719	    const anchorCoords =
720	      anchor === element
721	        ? null
722	        : getElementAbsoluteCoords(anchor, allElementsMap);
723	    const anchorSceneX = anchorCoords?.[0] ?? x1;
724	    const anchorSceneY = anchorCoords?.[1] ?? y1;
725	    const anchorPadding =
726	      anchor === element ? padding : getCanvasPadding(anchor);
727	    const anchorX =
728	      (anchorSceneX + appState.scrollX) * devicePixelRatio - anchorPadding;
729	    const anchorY =
730	      (anchorSceneY + appState.scrollY) * devicePixelRatio - anchorPadding;
731	
732	    // Form the relative vector before introducing the scroll translation.
733	    const dx = (x1 - anchorSceneX) * devicePixelRatio + anchorPadding - padding;
734	    const dy = (y1 - anchorSceneY) * devicePixelRatio + anchorPadding - padding;
735	    context.setTransform(
736	      a,
737	      b,
738	      c,
739	      d,
740	      Math.round(a * anchorX + c * anchorY + e) +
741	        Math.round(a * dx + c * dy + SNAP_TIE_BIAS),
742	      Math.round(b * anchorX + d * anchorY + f) +
743	        Math.round(b * dx + d * dy + SNAP_TIE_BIAS),
744	    );
745	    drawX = 0;
746	    drawY = 0;
747	  }
748	
749	  context.drawImage(
750	    elementWithCanvas.canvas!,
751	    drawX,
752	    drawY,
753	    elementWithCanvas.canvas!.width / elementWithCanvas.scale,
754	    elementWithCanvas.canvas!.height / elementWithCanvas.scale,
755	  );
756	
757	  context.setTransform(transform);
758	
759	  if (
760	    import.meta.env.VITE_APP_DEBUG_ENABLE_TEXT_CONTAINER_BOUNDING_BOX ===
761	      "true" &&
762	    hasBoundTextElement(element)
763	  ) {
764	    const textElement = getBoundTextElement(
765	      element,
766	      allElementsMap,
767	    ) as ExcalidrawTextElementWithContainer;
768	    const coords = getContainerCoords(element);
769	    context.strokeStyle = "#c92a2a";
770	    context.lineWidth = 3;
771	    context.strokeRect(
772	      (coords.x + appState.scrollX) * devicePixelRatio,
773	      (coords.y + appState.scrollY) * devicePixelRatio,
774	      getBoundTextMaxWidth(element, textElement) * devicePixelRatio,
775	      getBoundTextMaxHeight(element, textElement) * devicePixelRatio,
776	    );
777	  }
778	  context.restore();
779	
780	  // Clear the nested element we appended to the DOM
781	};
782	
783	export const renderSelectionElement = (
784	  element: NonDeletedExcalidrawElement,
785	  context: CanvasRenderingContext2D,
786	  appState: InteractiveCanvasAppState,
787	  selectionColor: InteractiveCanvasRenderConfig["selectionColor"],
788	) => {
789	  context.save();
790	  context.translate(element.x + appState.scrollX, element.y + appState.scrollY);
791	  context.fillStyle = applyDarkModeFilter(
792	    "rgba(0, 0, 200, 0.04)",
793	    appState.theme === THEME.DARK,
794	  );
795	
796	  // render from 0.5px offset  to get 1px wide line
797	  // https://stackoverflow.com/questions/7530593/html5-canvas-and-line-width/7531540#7531540
798	  // TODO can be be improved by offseting to the negative when user selects
799	  // from right to left
800	  const offset = 0.5 / appState.zoom.value;
801	
802	  context.fillRect(offset, offset, element.width, element.height);
803	  context.lineWidth = 1 / appState.zoom.value;
804	  context.strokeStyle = selectionColor;
805	  context.strokeRect(offset, offset, element.width, element.height);
806	
807	  context.restore();
808	};
809	
810	export const renderElement = (
811	  element: NonDeletedExcalidrawElement,
812	  elementsMap: RenderableElementsMap,
813	  allElementsMap: NonDeletedSceneElementsMap,
814	  rc: RoughCanvas,
815	  context: CanvasRenderingContext2D,
816	  renderConfig: StaticCanvasRenderConfig,
817	  appState: StaticCanvasAppState | InteractiveCanvasAppState,
818	) => {
819	  const reduceAlphaForSelection =
820	    appState.openDialog?.name === "elementLinkSelector" &&
821	    !appState.selectedElementIds[element.id] &&
822	    !appState.hoveredElementIds[element.id];
823	
824	  context.globalAlpha = getRenderOpacity(
825	    element,
826	    getContainingFrame(element, elementsMap),
827	    renderConfig.elementsPendingErasure,
828	    renderConfig.pendingFlowchartNodes,
829	    reduceAlphaForSelection ? DEFAULT_REDUCED_GLOBAL_ALPHA : 1,
830	  );
831	
832	  switch (element.type) {
833	    case "magicframe":
834	    case "frame": {
835	      if (appState.frameRendering.enabled && appState.frameRendering.outline) {
836	        context.save();
837	        context.translate(
838	          element.x + appState.scrollX,
839	          element.y + appState.scrollY,
840	        );
841	        context.fillStyle = "rgba(0, 0, 200, 0.04)";
842	
843	        context.lineWidth = FRAME_STYLE.strokeWidth / appState.zoom.value;
844	        context.strokeStyle = applyDarkModeFilter(
845	          FRAME_STYLE.strokeColor,
846	          appState.theme === THEME.DARK,
847	        );
848	
849	        // TODO change later to only affect AI frames
```

## 14. `Read` (sub-agent)

```json
{
 "file_path": "C:\\work\\excalidraw\\packages\\element\\src\\Scene.ts",
 "offset": 260,
 "limit": 150
}
```
**result of 14**
```
260	      if (nextElement !== element) {
261	        didChange = true;
262	      }
263	      return nextElement;
264	    });
265	    if (didChange) {
266	      this.replaceAllElements(newElements);
267	    }
268	    return didChange;
269	  }
270	
271	  replaceAllElements(
272	    nextElements: ElementsMapOrArray,
273	    options?: {
274	      skipValidation?: true;
275	    },
276	  ) {
277	    // we do trust the insertion order on the map, though maybe we shouldn't and should prefer order defined by fractional indices
278	    const _nextElements = toArray(nextElements);
279	    const nextFrameLikes: ExcalidrawFrameLikeElement[] = [];
280	
281	    if (!options?.skipValidation) {
282	      validateIndicesThrottled(_nextElements);
283	    }
284	
285	    this.elements = syncInvalidIndices(_nextElements);
286	    this.elementsMap.clear();
287	    this.elements.forEach((element) => {
288	      if (isFrameLikeElement(element)) {
289	        nextFrameLikes.push(element);
290	      }
291	      this.elementsMap.set(element.id, element);
292	    });
293	    const nonDeletedElements = getNonDeletedElements(this.elements);
294	    this.nonDeletedElements = nonDeletedElements.elements;
295	    this.nonDeletedElementsMap = nonDeletedElements.elementsMap;
296	
297	    this.frames = nextFrameLikes;
298	    this.nonDeletedFramesLikes = getNonDeletedElements(this.frames).elements;
299	
300	    this.triggerUpdate();
301	  }
302	
303	  triggerUpdate() {
304	    this.sceneNonce = randomInteger();
305	
306	    for (const callback of Array.from(this.callbacks)) {
307	      callback();
308	    }
309	  }
310	
311	  onUpdate(cb: SceneStateCallback): SceneStateCallbackRemover {
312	    if (this.callbacks.has(cb)) {
313	      throw new Error();
314	    }
315	
316	    this.callbacks.add(cb);
317	
318	    return () => {
319	      if (!this.callbacks.has(cb)) {
320	        throw new Error();
321	      }
322	      this.callbacks.delete(cb);
323	    };
324	  }
325	
326	  destroy() {
327	    this.elements = [];
328	    this.nonDeletedElements = [];
329	    this.nonDeletedFramesLikes = [];
330	    this.frames = [];
331	    this.elementsMap.clear();
332	    this.selectedElementsCache.selectedElementIds = null;
333	    this.selectedElementsCache.elements = null;
334	    this.selectedElementsCache.cache.clear();
335	
336	    // done not for memory leaks, but to guard against possible late fires
337	    // (I guess?)
338	    this.callbacks.clear();
339	  }
340	
341	  /** low-level - generally use app.insertNewElements() */
342	  insertElementsAtIndex(
343	    elements: ExcalidrawElement[],
344	    /** null indicates end of the array */
345	    index: number | null,
346	  ) {
347	    if (!elements.length) {
348	      return;
349	    }
350	
351	    if (index === null) {
352	      index = this.elements.length;
353	    }
354	
355	    if (!Number.isFinite(index) || index < 0) {
356	      throw new Error(
357	        "insertElementAtIndex can only be called with index >= 0",
358	      );
359	    }
360	
361	    const nextElements = [
362	      ...this.elements.slice(0, index),
363	      ...elements,
364	      ...this.elements.slice(index),
365	    ];
366	
367	    syncMovedIndices(nextElements, arrayToMap(elements));
368	
369	    this.replaceAllElements(nextElements);
370	  }
371	
372	  /** low-level - generally use app.insertNewElement() */
373	  insertElement = (element: ExcalidrawElement) => {
374	    this.insertElementsAtIndex([element], null);
375	  };
376	
377	  getElementIndex(elementId: string) {
378	    return this.elements.findIndex((element) => element.id === elementId);
379	  }
380	
381	  getContainerElement = (
382	    element:
383	      | (ExcalidrawElement & {
384	          containerId: ExcalidrawElement["id"] | null;
385	        })
386	      | null,
387	  ) => {
388	    if (!element) {
389	      return null;
390	    }
391	    if (element.containerId) {
392	      return this.getElement(element.containerId) || null;
393	    }
394	    return null;
395	  };
396	
397	  getElementsFromId = (id: string): ExcalidrawElement[] => {
398	    const elementsMap = this.getNonDeletedElementsMap();
399	    // first check if the id is an element
400	    const el = elementsMap.get(id);
401	    if (el) {
402	      return [el];
403	    }
404	
405	    // then, check if the id is a group
406	    return getElementsInGroup(elementsMap, id);
407	  };
408	
409	  // Mutate an element with passed updates and trigger the component to update. Make sure you
```

## 15. `Bash` (sub-agent)

```json
{
 "command": "cd \"C:\\work\\excalidraw\" && grep -n \"export const throttleRAF\\|function throttleRAF\" -A 40 packages/common/src/utils.ts | head -60",
 "description": "Find throttleRAF implementation"
}
```
**result of 15**
```
184:export const throttleRAF = <T extends any[]>(fn: (...args: T) => void) => {
185-  let timerId: number | null = null;
186-  let lastArgs: T | null = null;
187-
188-  const scheduleFunc = () => {
189-    timerId = window.requestAnimationFrame(() => {
190-      timerId = null;
191-      const args = lastArgs;
192-      lastArgs = null;
193-
194-      if (args) {
195-        fn(...args);
196-      }
197-    });
198-  };
199-
200-  const ret = (...args: T) => {
201-    lastArgs = args;
202-    if (timerId === null) {
203-      scheduleFunc();
204-    }
205-  };
206-  ret.flush = () => {
207-    if (timerId !== null) {
208-      cancelAnimationFrame(timerId);
209-      timerId = null;
210-    }
211-    if (lastArgs) {
212-      fn(...lastArgs);
213-      lastArgs = null;
214-    }
215-  };
216-  ret.cancel = () => {
217-    lastArgs = null;
218-    if (timerId !== null) {
219-      cancelAnimationFrame(timerId);
220-      timerId = null;
221-    }
222-  };
223-  return ret;
224-};
```

## 16. `Grep` (sub-agent)

```json
{
 "pattern": "version\\+\\+|versionNonce|bumpVersion|incrementVersion\" \"packages/element/src/mutateElement.ts",
 "path": "C:\\work\\excalidraw\\packages\\element\\src\\mutateElement.ts",
 "output_mode": "content",
 "-n": true
}
```
**result of 16**
```
143:  element.versionNonce = updates.versionNonce ?? randomInteger();
178:    versionNonce: updates.versionNonce ?? randomInteger(),
184: * Mutates element, bumping `version`, `versionNonce`, and `updated`.
188:export const bumpVersion = <T extends Mutable<ExcalidrawElement>>(
193:  element.versionNonce = randomInteger();
```

## 17. `Read` (sub-agent)

```json
{
 "file_path": "C:\\work\\excalidraw\\packages\\element\\src\\mutateElement.ts",
 "offset": 1,
 "limit": 200
}
```
**result of 17**
```
1	import {
2	  getSizeFromPoints,
3	  randomInteger,
4	  getUpdatedTimestamp,
5	} from "@excalidraw/common";
6	
7	import type { Radians } from "@excalidraw/math";
8	
9	import type { Mutable } from "@excalidraw/common/utility-types";
10	
11	import { ShapeCache } from "./shape";
12	
13	import { updateElbowArrowPoints } from "./elbowArrow";
14	
15	import { isElbowArrow } from "./typeChecks";
16	
17	import type {
18	  ElementsMap,
19	  ExcalidrawElbowArrowElement,
20	  ExcalidrawElement,
21	  NonDeletedSceneElementsMap,
22	} from "./types";
23	
24	// `created` is lifetime metadata: it is set once when an element instance is
25	// constructed (or duplicated) and never updated, so it is not part of an
26	// element update. An explicit repair must construct a new element object.
27	export type ElementUpdate<TElement extends ExcalidrawElement> = Omit<
28	  Partial<TElement>,
29	  "id" | "updated" | "created"
30	>;
31	
32	/**
33	 * This function tracks updates of text elements for the purposes for collaboration.
34	 * The version is used to compare updates when more than one user is working in
35	 * the same drawing.
36	 *
37	 * WARNING: this won't trigger the component to update, so if you need to trigger component update,
38	 * use `scene.mutateElement` or `ExcalidrawImperativeAPI.mutateElement` instead.
39	 */
40	export const mutateElement = <TElement extends Mutable<ExcalidrawElement>>(
41	  element: TElement,
42	  elementsMap: ElementsMap,
43	  updates: ElementUpdate<TElement>,
44	  options?: {
45	    isDragging?: boolean;
46	    isBindingEnabled?: boolean;
47	    isMidpointSnappingEnabled?: boolean;
48	  },
49	) => {
50	  let didChange = false;
51	
52	  // casting to any because can't use `in` operator
53	  // (see https://github.com/microsoft/TypeScript/issues/21732)
54	  const { points, fixedSegments, fileId } = updates as any;
55	
56	  if (
57	    isElbowArrow(element) &&
58	    (Object.keys(updates).length === 0 || // normalization case
59	      typeof points !== "undefined" || // repositioning
60	      typeof fixedSegments !== "undefined") // segment fixing
61	  ) {
62	    updates = {
63	      ...updates,
64	      angle: 0 as Radians,
65	      ...updateElbowArrowPoints(
66	        {
67	          ...(element as ExcalidrawElbowArrowElement),
68	          x: updates.x || element.x,
69	          y: updates.y || element.y,
70	        },
71	        elementsMap as NonDeletedSceneElementsMap,
72	        updates as ElementUpdate<ExcalidrawElbowArrowElement>,
73	        options,
74	      ),
75	    };
76	  } else if (typeof points !== "undefined") {
77	    updates = { ...getSizeFromPoints(points), ...updates };
78	  }
79	
80	  for (const key in updates) {
81	    const value = (updates as any)[key];
82	    if (typeof value !== "undefined") {
83	      if (
84	        (element as any)[key] === value &&
85	        // if object, always update because its attrs could have changed
86	        // (except for specific keys we handle below)
87	        (typeof value !== "object" ||
88	          value === null ||
89	          key === "groupIds" ||
90	          key === "scale")
91	      ) {
92	        continue;
93	      }
94	
95	      if (key === "scale") {
96	        const prevScale = (element as any)[key];
97	        const nextScale = value;
98	        if (prevScale[0] === nextScale[0] && prevScale[1] === nextScale[1]) {
99	          continue;
100	        }
101	      } else if (key === "points") {
102	        const prevPoints = (element as any)[key];
103	        const nextPoints = value;
104	        if (prevPoints.length === nextPoints.length) {
105	          let didChangePoints = false;
106	          let index = prevPoints.length;
107	          while (--index) {
108	            const prevPoint = prevPoints[index];
109	            const nextPoint = nextPoints[index];
110	            if (
111	              prevPoint[0] !== nextPoint[0] ||
112	              prevPoint[1] !== nextPoint[1]
113	            ) {
114	              didChangePoints = true;
115	              break;
116	            }
117	          }
118	          if (!didChangePoints) {
119	            continue;
120	          }
121	        }
122	      }
123	
124	      (element as any)[key] = value;
125	      didChange = true;
126	    }
127	  }
128	
129	  if (!didChange) {
130	    return element;
131	  }
132	
133	  if (
134	    typeof updates.height !== "undefined" ||
135	    typeof updates.width !== "undefined" ||
136	    typeof fileId != "undefined" ||
137	    typeof points !== "undefined"
138	  ) {
139	    ShapeCache.delete(element);
140	  }
141	
142	  element.version = updates.version ?? element.version + 1;
143	  element.versionNonce = updates.versionNonce ?? randomInteger();
144	  element.updated = getUpdatedTimestamp();
145	
146	  return element;
147	};
148	
149	export const newElementWith = <TElement extends ExcalidrawElement>(
150	  element: TElement,
151	  updates: ElementUpdate<TElement>,
152	  /** pass `true` to always regenerate */
153	  force = false,
154	): TElement => {
155	  let didChange = false;
156	  for (const key in updates) {
157	    const value = (updates as any)[key];
158	    if (typeof value !== "undefined") {
159	      if (
160	        (element as any)[key] === value &&
161	        // if object, always update because its attrs could have changed
162	        (typeof value !== "object" || value === null)
163	      ) {
164	        continue;
165	      }
166	      didChange = true;
167	    }
168	  }
169	
170	  if (!didChange && !force) {
171	    return element;
172	  }
173	
174	  return {
175	    ...element,
176	    ...updates,
177	    version: updates.version ?? element.version + 1,
178	    versionNonce: updates.versionNonce ?? randomInteger(),
179	    updated: getUpdatedTimestamp(),
180	  };
181	};
182	
183	/**
184	 * Mutates element, bumping `version`, `versionNonce`, and `updated`.
185	 *
186	 * NOTE: does not trigger re-render.
187	 */
188	export const bumpVersion = <T extends Mutable<ExcalidrawElement>>(
189	  element: T,
190	  version?: ExcalidrawElement["version"],
191	) => {
192	  element.version = (version ?? element.version) + 1;
193	  element.versionNonce = randomInteger();
194	  element.updated = getUpdatedTimestamp();
195	  return element;
196	};
197	
```

## 18. `Bash` (sub-agent)

```json
{
 "command": "cd \"C:\\work\\excalidraw\" && grep -n \"renderStaticScene\\|renderInteractiveScene\\|triggerRender\\|scheduleUpdate\\|requestAnimationFrame\\|new Scene(\\|this.scene =\\|StaticCanvas\\|InteractiveCanvas\" packages/excalidraw/components/App.tsx | head -80",
 "description": "Find App.tsx render scheduling hooks"
}
```
**result of 18**
```
450:import { StaticCanvas, InteractiveCanvas } from "./canvases";
873:    this.scene = new Scene();
1073:    this.triggerRender();
2580:                          <StaticCanvas
2631:                          <InteractiveCanvas
2651:                            renderInteractiveSceneCallback={
2652:                              this.renderInteractiveSceneCallback
2654:                            handleCanvasRef={this.handleInteractiveCanvasRef}
2787:    this.triggerRender();
3765:    this.scene.onUpdate(this.triggerRender);
3839:    this.scene = new Scene();
3932:          this.triggerRender(true);
4342:  private renderInteractiveSceneCallback = ({
5338:  public triggerRender = (
8233:    this.triggerRender();
8605:          this.ownerWindow.requestAnimationFrame(() => {
12545:    this.triggerRender();
12934:  private handleInteractiveCanvasRef = (canvas: HTMLCanvasElement | null) => {
```

## 19. `Bash` (sub-agent)

```json
{
 "command": "cd \"C:\\work\\excalidraw\" && sed -n '5330,5370p' packages/excalidraw/components/App.tsx",
 "description": "Read triggerRender method"
}
```
**result of 19**
```
    informMutation = true,
  ) => {
    return this.scene.mutateElement(element, updates, {
      informMutation,
      isDragging: false,
    });
  };

  public triggerRender = (
    /** force always re-renders canvas even if no change */
    force?: boolean,
  ) => {
    if (force === true) {
      this.scene.triggerUpdate();
    } else {
      this.setState({});
    }
  };

  /**
   * @returns whether the menu was toggled on or off
   */
  public toggleSidebar = ({
    name,
    tab,
    force,
  }: {
    name: SidebarName | null;
    tab?: SidebarTabName;
    force?: boolean;
  }): boolean => {
    let nextName;
    if (force === undefined) {
      nextName =
        this.state.openSidebar?.name === name &&
        this.state.openSidebar?.tab === tab
          ? null
          : name;
    } else {
      nextName = force ? name : null;
    }
```

## 20. `Bash` (sub-agent)

```json
{
 "command": "cd \"C:\\work\\excalidraw\" && find packages/excalidraw/components -iname \"canvases*\"",
 "description": "Locate canvases component file"
}
```
**result of 20**
```
packages/excalidraw/components/canvases
```

## 21. `Glob` (sub-agent)

```json
{
 "pattern": "packages/excalidraw/components/canvases/*"
}
```
**result of 21**
```
packages\excalidraw\components\canvases\index.tsx
packages\excalidraw\components\canvases\InteractiveCanvas.tsx
packages\excalidraw\components\canvases\NewElementCanvas.tsx
packages\excalidraw\components\canvases\StaticCanvas.tsx
```

## 22. `Read` (sub-agent)

```json
{
 "file_path": "C:\\work\\excalidraw\\packages\\excalidraw\\components\\canvases\\StaticCanvas.tsx"
}
```
**result of 22**
```
1	import React, { useEffect, useRef } from "react";
2	
3	import { isShallowEqual } from "@excalidraw/common";
4	
5	import type {
6	  NonDeletedExcalidrawElement,
7	  NonDeletedSceneElementsMap,
8	} from "@excalidraw/element/types";
9	
10	import { isRenderThrottlingEnabled } from "../../reactUtils";
11	import { renderStaticScene } from "../../renderer/staticScene";
12	
13	import type {
14	  RenderableElementsMap,
15	  StaticCanvasRenderConfig,
16	} from "../../scene/types";
17	import type { AppState, StaticCanvasAppState } from "../../types";
18	import type { RoughCanvas } from "roughjs/bin/canvas";
19	
20	type StaticCanvasProps = {
21	  canvas: HTMLCanvasElement;
22	  rc: RoughCanvas;
23	  elementsMap: RenderableElementsMap;
24	  allElementsMap: NonDeletedSceneElementsMap;
25	  visibleElements: readonly NonDeletedExcalidrawElement[];
26	  canvasNonce: string;
27	  selectionNonce: number | undefined;
28	  scale: number;
29	  appState: StaticCanvasAppState;
30	  renderConfig: StaticCanvasRenderConfig;
31	};
32	
33	const StaticCanvas = (props: StaticCanvasProps) => {
34	  const wrapperRef = useRef<HTMLDivElement>(null);
35	  const isComponentMounted = useRef(false);
36	
37	  useEffect(() => {
38	    props.canvas.style.width = `${props.appState.width}px`;
39	    props.canvas.style.height = `${props.appState.height}px`;
40	    props.canvas.width = props.appState.width * props.scale;
41	    props.canvas.height = props.appState.height * props.scale;
42	  }, [props.appState.height, props.appState.width, props.canvas, props.scale]);
43	
44	  useEffect(() => {
45	    const wrapper = wrapperRef.current;
46	    if (!wrapper) {
47	      return;
48	    }
49	
50	    const canvas = props.canvas;
51	
52	    if (!isComponentMounted.current) {
53	      isComponentMounted.current = true;
54	
55	      wrapper.replaceChildren(canvas);
56	      canvas.classList.add("excalidraw__canvas", "static");
57	    }
58	
59	    renderStaticScene(
60	      {
61	        canvas,
62	        rc: props.rc,
63	        scale: props.scale,
64	        elementsMap: props.elementsMap,
65	        allElementsMap: props.allElementsMap,
66	        visibleElements: props.visibleElements,
67	        appState: props.appState,
68	        renderConfig: props.renderConfig,
69	      },
70	      isRenderThrottlingEnabled(),
71	    );
72	  });
73	
74	  return <div className="excalidraw__canvas-wrapper" ref={wrapperRef} />;
75	};
76	
77	const getRelevantAppStateProps = (appState: AppState): StaticCanvasAppState => {
78	  const relevantAppStateProps = {
79	    zoom: appState.zoom,
80	    scrollX: appState.scrollX,
81	    scrollY: appState.scrollY,
82	    width: appState.width,
83	    height: appState.height,
84	    viewModeEnabled: appState.viewModeEnabled,
85	    openDialog: appState.openDialog,
86	    hoveredElementIds: appState.hoveredElementIds,
87	    offsetLeft: appState.offsetLeft,
88	    offsetTop: appState.offsetTop,
89	    theme: appState.theme,
90	    shouldCacheIgnoreZoom: appState.shouldCacheIgnoreZoom,
91	    viewBackgroundColor: appState.viewBackgroundColor,
92	    exportScale: appState.exportScale,
93	    selectedElementsAreBeingDragged: appState.selectedElementsAreBeingDragged,
94	    gridSize: appState.gridSize,
95	    gridStep: appState.gridStep,
96	    frameRendering: appState.frameRendering,
97	    selectedElementIds: appState.selectedElementIds,
98	    frameToHighlight: appState.frameToHighlight,
99	    editingGroupId: appState.editingGroupId,
100	    currentHoveredFontFamily: appState.currentHoveredFontFamily,
101	    croppingElementId: appState.croppingElementId,
102	    suggestedBinding: appState.suggestedBinding,
103	  };
104	
105	  return relevantAppStateProps;
106	};
107	
108	const areEqual = (
109	  prevProps: StaticCanvasProps,
110	  nextProps: StaticCanvasProps,
111	) => {
112	  if (
113	    prevProps.canvasNonce !== nextProps.canvasNonce ||
114	    prevProps.scale !== nextProps.scale ||
115	    // we need to memoize on elementsMap because they may have renewed
116	    // even if canvasNonce didn't change (e.g. we filter elements out based
117	    // on appState)
118	    prevProps.elementsMap !== nextProps.elementsMap ||
119	    prevProps.visibleElements !== nextProps.visibleElements
120	  ) {
121	    return false;
122	  }
123	
124	  return (
125	    isShallowEqual(
126	      // asserting AppState because we're being passed the whole AppState
127	      // but resolve to only the StaticCanvas-relevant props
128	      getRelevantAppStateProps(prevProps.appState as AppState),
129	      getRelevantAppStateProps(nextProps.appState as AppState),
130	    ) && isShallowEqual(prevProps.renderConfig, nextProps.renderConfig)
131	  );
132	};
133	
134	export default React.memo(StaticCanvas, areEqual);
135	
```

> I have everything I need. Let me compose the report.
> 
> ## How Excalidraw Renders and Updates Canvas Elements
> 
> ### 1. Rendering entry points (`packages/excalidraw/renderer/`)
> 
> Excalidraw uses **two stacked `<canvas>` elements**, each with its own render pipeline:
> 
> - **Static canvas** — `packages/excalidraw/renderer/staticScene.ts`
>   - `_renderStaticScene` (line 261) is the actual paint routine: draws the grid (`strokeGrid`, line 61), then iterates `visibleElements` calling `renderElement` for each (lines 317-515), handling frame clipping, bound text, embeddables, and link icons.
>   - `renderStaticSceneThrottled` (line 519) wraps it in `throttleRAF` (rAF-batched).
>   - `renderStaticScene(renderConfig, throttle?)` (line 528) is the public entry; `throttle=true` goes through the rAF-throttled path, otherwise calls `_renderStaticScene` synchronously (used for exports/snapshots).
> - **Interactive canvas** — `packages/excalidraw/renderer/interactiveScene.ts`
>   - `renderInteractiveScene` (line 2165) draws selection boxes, transform handles, remote cursors, scrollbars, snapping guides, binding highlights — i.e., everything that is UI chrome rather than actual drawing content.
>   - Also rAF-throttled similarly to the static scene.
> - React wiring: `packages/excalidraw/components/canvases/StaticCanvas.tsx` and `InteractiveCanvas.tsx` are `React.memo`'d components whose `useEffect` calls `renderStaticScene(...)` / the interactive equivalent on every relevant prop change, gated with a custom `areEqual` comparator (StaticCanvas.tsx:108-132) that short-circuits on `canvasNonce`, `scale`, `elementsMap`, `visibleElements` identity and a shallow compare of the relevant `AppState` subset.
> 
> ### 2. Element storage / Scene class (`packages/element/src/Scene.ts`)
> 
> - `class Scene` (Scene.ts:108) holds `private elements: readonly OrderedExcalidrawElement[]` (121) and a `private elementsMap` (`SceneElementsMap`, 125), plus derived `nonDeletedElements`/`nonDeletedElementsMap`/`frames`.
> - `replaceAllElements()` (271) is the core mutation path: rebuilds the array/map, derives non-deleted elements and frames, then calls `this.triggerUpdate()` (300).
> - `triggerUpdate()` (303) sets `this.sceneNonce = randomInteger()` (304) and invokes all registered `callbacks` (306-308) — this is the pub/sub mechanism Scene uses to notify the app.
> - `onUpdate(cb)` (311) registers a callback; App.tsx wires `this.scene.onUpdate(this.triggerRender)` (App.tsx:3765).
> - `Renderer` class (`packages/excalidraw/scene/Renderer.ts`) sits on top of `Scene` and computes the per-frame renderable set: `getVisibleCanvasElements` (47) viewport-culls via `isElementInViewport`, `getRenderableElementsMap` (89) excludes the element currently being text-edited, and `_getRenderableElements` (159) is wrapped in `memoize` keyed on a `canvasNonce` (derived from `scene.getSceneNonce()` + zoom/scroll/size/editing state) so repeated calls with identical inputs are free.
> 
> ### 3. Static vs. interactive canvas split
> 
> Confirmed distinct canvases: static canvas (`staticScene.ts`) renders actual scene content (shapes, grid, frames, embeddables, bound text) and is meant to be cached/bitmap-friendly; interactive canvas (`interactiveScene.ts`) renders selection outlines, transform handles, remote cursors, scrollbars (`../scene/scrollbars`), snap guides (`renderSnaps`) — ephemeral UI that changes far more often (every mouse move) and must not force a repaint of all elements. There's also `renderNewElementScene.ts` for the element currently being drawn and `NewElementCanvas.tsx` as a third layer.
> 
> ### 4. Update triggering
> 
> - `App.triggerRender(force?)` (App.tsx:5338) either calls `this.scene.triggerUpdate()` (force path) or `this.setState({})` to cause a React re-render, which flows props down into the memoized `StaticCanvas`/`InteractiveCanvas` components.
> - `Scene.onUpdate(this.triggerRender)` is registered once in App's constructor-equivalent (App.tsx:3765), so any scene mutation (`replaceAllElements`) automatically triggers a render.
> - Actual canvas painting is rAF-batched via `throttleRAF` (`packages/common/src/utils.ts:184-224`): it coalesces calls within an animation frame, keeping only the latest args (`lastArgs`), and exposes `.flush()`/`.cancel()`. `isRenderThrottlingEnabled()` (`packages/excalidraw/reactUtils`) decides whether `StaticCanvas` passes `throttle=true`.
> 
> ### 5. Per-element drawing / dispatch (`packages/element/src/renderElement.ts`)
> 
> - `renderElement(element, elementsMap, allElementsMap, rc, context, renderConfig, appState)` (line 810) is the dispatcher: sets `context.globalAlpha` via `getRenderOpacity`, then `switch (element.type)` (line 832) handles `frame`/`magicframe`, and (further down, not fully shown) rectangle/diamond/ellipse/text/image/freedraw/line/arrow/iframe/embeddable cases, generally calling into roughjs-drawn shapes or `context.drawImage` for cached bitmaps.
> - **Shape cache**: `class ShapeCache` (`packages/element/src/shape.ts:82`) is a `WeakMap<ExcalidrawElement, {shape, theme}>` (84-87). `ShapeCache.generateElementShape()` (119) returns the cached rough shape unless exporting or theme mismatches, otherwise calls `_generateElementShape` (752) which builds roughjs `Drawable`s per type (rectangle/diamond/ellipse/line/arrow/freedraw) and caches the result (156-161). `ShapeCache.delete()` (106) also clears `elementWithCanvasCache`.
> - **Element-bitmap cache**: `elementWithCanvasCache` (renderElement.ts:534), a `WeakMap<ExcalidrawElement, ExcalidrawElementWithCanvas>`. `generateElementWithCanvas` (539) only regenerates the offscreen canvas bitmap when zoom/theme/imageCrop/frame-opacity changed (560-566); `drawElementFromCanvas` (618) blits that cached bitmap onto the real context with device-pixel snapping logic for crisp unrotated/right-angle elements (`canSnapElement`, 603).
> 
> ### 6. roughjs usage
> 
> `packages/element/src/shape.ts` imports `RoughGenerator` from `roughjs/bin/generator` (line 31) and is the sole place rough shapes are generated (`generator.rectangle/polygon/ellipse/curve/path/linearPath/circle`, e.g. lines 780-868). `renderElement.ts`/`staticScene.ts` receive a `RoughCanvas` (`rc`, from `roughjs/bin/canvas`) used to actually stroke/fill those `Drawable`s onto the `CanvasRenderingContext2D`. Freedraw uses `perfect-freehand` (`getStroke`/`getStrokePoints`) and `@excalidraw/laser-pointer` instead of roughjs, producing an SVG path (`getFreeDrawSvgPath`, shape.ts:1169).
> 
> ### 7. Dirty-checking / invalidation
> 
> Three layered mechanisms avoid wasted work:
> - **Element-level version**: `mutateElement()` (`packages/element/src/mutateElement.ts:40`) only applies changes if a value actually differs (84-122), then bumps `element.version`/`element.versionNonce`/`element.updated` (142-144) and calls `ShapeCache.delete(element)` when width/height/fileId/points changed (133-140) to force shape regeneration. `bumpVersion` (188) and `newElementWith` (149) do analogous version bumps elsewhere.
> - **Scene-level nonce**: `Scene.triggerUpdate()` assigns a new `sceneNonce` (Scene.ts:304) any time elements are replaced; `Renderer.getRenderableElements` combines this with zoom/scroll/size/editing state into a `canvasNonce` string (Renderer.ts:210-212) used as the memoization key.
> - **React-level memoization**: `StaticCanvas`'s `areEqual` (StaticCanvas.tsx:108) and the WeakMap caches (`ShapeCache`, `elementWithCanvasCache`) prevent re-generating roughjs geometry or re-rastering bitmaps unless the relevant inputs (version, zoom, theme, crop, frame opacity) changed.

> ## How Excalidraw renders and updates canvas elements
> 
> Excalidraw uses **two stacked `<canvas>` layers** rather than one, so cheap UI chrome doesn't force expensive redraws of actual content:
> 
> **1. Static canvas** — `packages/excalidraw/renderer/staticScene.ts`
> Paints the actual scene: grid, shapes, frames, bound text, embeddables. `_renderStaticScene` (line 261) iterates visible elements and calls `renderElement` for each. The public entry `renderStaticScene()` (528) either runs synchronously (for exports) or through `renderStaticSceneThrottled` (519), which is rAF-batched.
> 
> **2. Interactive canvas** — `packages/excalidraw/renderer/interactiveScene.ts`
> Paints selection boxes, transform handles, remote cursors, scrollbars, snap guides — everything that changes on every mouse move but isn't actual drawn content. Kept separate so cursor movement doesn't repaint all shapes.
> 
> Both are wired into React via `StaticCanvas.tsx`/`InteractiveCanvas.tsx`, memoized components whose `useEffect` triggers the render functions, gated by a custom `areEqual` that checks a `canvasNonce`, scale, and element-map identity before re-rendering.
> 
> **Element storage**: `packages/element/src/Scene.ts` holds the element array/map. `replaceAllElements()` (271) rebuilds state and calls `triggerUpdate()` (303), which bumps a `sceneNonce` and fires subscriber callbacks — `App.tsx` subscribes via `scene.onUpdate(this.triggerRender)`. A `Renderer` class on top (`packages/excalidraw/scene/Renderer.ts`) viewport-culls elements and memoizes the visible set keyed on that nonce plus zoom/scroll/size.
> 
> **Per-element drawing**: `renderElement()` in `packages/element/src/renderElement.ts` (810) dispatches by `element.type`. Shapes are drawn via **roughjs** (for the hand-drawn look) with geometry built once and cached in `ShapeCache` (`shape.ts:82`, a `WeakMap<element, shape>`). Rendered bitmaps are further cached per-element in `elementWithCanvasCache` and only regenerated when zoom/theme/crop changes — otherwise just blitted with `drawImage`, snapped to device pixels. Freedraw uses `perfect-freehand` instead of roughjs.
> 
> **Invalidation**: `mutateElement()` (`packages/element/src/mutateElement.ts:40`) only bumps `element.version`/`versionNonce` when a value actually changed, and clears the shape cache when geometry-affecting props change. This version bump propagates up through the scene nonce → canvas nonce → React memo chain, so only genuinely changed elements get regenerated/repainted, while updates are coalesced per animation frame via a shared `throttleRAF` utility.

## Final answer

## How Excalidraw renders and updates canvas elements

Excalidraw uses **two stacked `<canvas>` layers** rather than one, so cheap UI chrome doesn't force expensive redraws of actual content:

**1. Static canvas** — `packages/excalidraw/renderer/staticScene.ts`
Paints the actual scene: grid, shapes, frames, bound text, embeddables. `_renderStaticScene` (line 261) iterates visible elements and calls `renderElement` for each. The public entry `renderStaticScene()` (528) either runs synchronously (for exports) or through `renderStaticSceneThrottled` (519), which is rAF-batched.

**2. Interactive canvas** — `packages/excalidraw/renderer/interactiveScene.ts`
Paints selection boxes, transform handles, remote cursors, scrollbars, snap guides — everything that changes on every mouse move but isn't actual drawn content. Kept separate so cursor movement doesn't repaint all shapes.

Both are wired into React via `StaticCanvas.tsx`/`InteractiveCanvas.tsx`, memoized components whose `useEffect` triggers the render functions, gated by a custom `areEqual` that checks a `canvasNonce`, scale, and element-map identity before re-rendering.

**Element storage**: `packages/element/src/Scene.ts` holds the element array/map. `replaceAllElements()` (271) rebuilds state and calls `triggerUpdate()` (303), which bumps a `sceneNonce` and fires subscriber callbacks — `App.tsx` subscribes via `scene.onUpdate(this.triggerRender)`. A `Renderer` class on top (`packages/excalidraw/scene/Renderer.ts`) viewport-culls elements and memoizes the visible set keyed on that nonce plus zoom/scroll/size.

**Per-element drawing**: `renderElement()` in `packages/element/src/renderElement.ts` (810) dispatches by `element.type`. Shapes are drawn via **roughjs** (for the hand-drawn look) with geometry built once and cached in `ShapeCache` (`shape.ts:82`, a `WeakMap<element, shape>`). Rendered bitmaps are further cached per-element in `elementWithCanvasCache` and only regenerated when zoom/theme/crop changes — otherwise just blitted with `drawImage`, snapped to device pixels. Freedraw uses `perfect-freehand` instead of roughjs.

**Invalidation**: `mutateElement()` (`packages/element/src/mutateElement.ts:40`) only bumps `element.version`/`versionNonce` when a value actually changed, and clears the shape cache when geometry-affecting props change. This version bump propagates up through the scene nonce → canvas nonce → React memo chain, so only genuinely changed elements get regenerated/repainted, while updates are coalesced per animation frame via a shared `throttleRAF` utility.
