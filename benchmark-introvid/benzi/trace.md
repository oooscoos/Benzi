# Benzi: tool-call trace

Question: **How does Excalidraw render and update canvas elements?**

21 tool calls, all Benzi's own. Source lines read: 43 (one `read_source`). Each result below is as recorded by the runner's log, which keeps the first 4,000 characters of a result; the model saw it whole.

## 1. `list_files`

```
{'path': 'packages', 'progress': 5}
```
**result**
```
dir: packages
subdirs[7,]{name,files}:
  common,27
  element,79
  excalidraw,436
  fractional-indexing,2
  laser-pointer,5
  math,26
  utils,8
files[0]:
```

## 2. `read_reference`

```
{'topic': 'artifact', 'progress': 5}
```
**result**
```
topic: artifact
text: "ARTIFACT DETAILS -- how the map fits together, and the tables your tools query.\n\nONE ID SCHEME, TWO FLOWS, JOINED:\n  - CALL FLOW is the edges: who calls whom (get_callers, find_call_path).\n  - DATA FLOW is the defs: every scope records each name's assignments as an\n    ORDERED sequence (reassignment is a sequence, not a mystery), each value\n    expression classified at compile time.\n  - The two flows JOIN at call sites -- an argument is where control and data\n    cross -- and trace_value_origin walks that join FOR you: through assignments, up the\n    call graph, to a value's origin. When a run crashed on a bad value,\n    trace_value_origin the function that choked before reasoning about causes; the\n    symptom usually surfaces layers away from the origin.\n\nEVERY SYMBOL CARRIES `symbolKind` -- the language's own word for it, named as\nLSP names it: Function, Method, Class, Struct, Enum, Interface, Trait, Record,\nModule, CssRule -- and a binding row (a local, field, or module constant)\ncarries symbolKind \"Binding\". Read it literally.\n\nTwo facts about edges that the kind alone will not tell you:\n  - An edge can LAND on a Class/Struct/Enum rather than a Function: that is\n    INSTANTIATION (\"who constructs this\"), where a constructor call resolves\n    when the type declares no constructor of its own. Ruby's `Type.new` reaches\n    `initialize` when the class or an ancestor has one, and the class itself\n    when it does not.\n  - A binding (a module constant, a field, a local) has an ordered assignment\n    history and data flow, and no call flow at all -- get_definition returns it\n    as a binding card, not a declaration card.\n\nTHE RESOLVED INDEX YOUR TOOLS QUERY -- everything keyed by ONE Benzi UID. Not a\nfile tree you walk; a set of UID-keyed tables you look up:\n  symbols{id}         DECLARATION -- what a thing IS: name, span, params,\n                      signature, decorators, docstring, fields   (get_definition)\n  edges               CALL FLOW, PROVEN     caller -> callee   (get_callers, find_call_path,\n                                                                 call_hierarchy for the whole chain)\n  candidate_edges     CALL FLOW, OVERRIDE DISPATCH  a call resolved to a base-class\n                                            method that has overrides -- which one runs\n                                            depends on the runtime type, undecidable\n                                            statically; running resolves it\n                                            (one hop: might_call/might_be_called_by on get_definition)\n  external_calls{id}  CALL FLOW, EXTERNAL   a scope's calls into third-party or\n                                            standard-library code, each with\n                                            `origin` (stdlib / dependency /\n                                            undeclared / unattributed) and `lib`\n                                            (list_external_calls -- raw call\n                                            sites, per file, per scope, or\n                                            omit for the whole repo (capped);\n                                            list_dependencies for the same\n                                            evidence deduped to library roots\n                                            with counts)\n  unresolved_calls{id} CALL FLOW, UNRESOLVED a scope's calls the compiler could not\n                                            settle, each with a `reason`:\n                                            opaque_receiver / untyped_local (no\n                                            target nameable); name_collision /\n                                            linkage_refused (2+ real in-repo\n                                            targets named in `candidates`, nothing\n                                            picked one -- a smarter static pass\n                                  
```

## 3. `list_files`

```
{'path': 'packages/excalidraw', 'progress': 15}
```
**result**
```
dir: packages/excalidraw
subdirs[14,]{name,files}:
  actions,46
  charts,8
  components,218
  context,2
  data,15
  eraser,1
  fonts,13
  hooks,12
  lasso,2
  renderer,9
  scene,6
  subset,7
  tests,63
  wysiwyg,2
files[32]:
  - path: packages/excalidraw/analytics.ts
    language: typescript
    line_count: 51
    docstring: place here categories that you want to track. We want to track just a
    symbols[1,]{id,symbolKind,line_span}:
      "packages/excalidraw/analytics.ts::trackEvent#Function",Function,12-50
    constants[1]: ALLOWED_CATEGORIES_TO_TRACK
  - path: packages/excalidraw/animatedTrail.ts
    language: typescript
    line_count: 223
    symbols[3,]{id,symbolKind,line_span}:
      "packages/excalidraw/animatedTrail.ts::Trail#Interface",Interface,15-22
      "packages/excalidraw/animatedTrail.ts::AnimatedTrailOptions#Interface",Interface,24-28
      "packages/excalidraw/animatedTrail.ts::AnimatedTrail#Class",Class,30-222
  - path: packages/excalidraw/appState.ts
    language: typescript
    line_count: 321
    symbols[8,]{id,symbolKind,line_span}:
      "packages/excalidraw/appState.ts::getDefaultAppState#Function",Function,23-139
      "packages/excalidraw/appState.ts::config#Function",Function,145-156
      "packages/excalidraw/appState.ts::_clearAppStateForStorage#Function",Function,272-294
      "packages/excalidraw/appState.ts::clearAppStateForLocalStorage#Function",Function,296-298
      "packages/excalidraw/appState.ts::cleanAppStateForExport#Function",Function,300-302
      "packages/excalidraw/appState.ts::clearAppStateForDatabase#Function",Function,304-306
      "packages/excalidraw/appState.ts::isEraserActive#Function",Function,308-312
      "packages/excalidraw/appState.ts::isHandToolActive#Function",Function,314-320
    constants[2]: APP_STATE_STORAGE_CONF,defaultExportScale
  - path: packages/excalidraw/charts.test.ts
    language: typescript
    line_count: 1167
    symbols[1,]{id,symbolKind,line_span}:
      "packages/excalidraw/charts.test.ts::describe callback#Function",Function,22-1166
  - path: packages/excalidraw/clients.ts
    language: typescript
    line_count: 259
    symbols[4,]{id,symbolKind,line_span}:
      "packages/excalidraw/clients.ts::hashToInteger#Function",Function,17-27
      "packages/excalidraw/clients.ts::getClientColor#Function",Function,29-43
      "packages/excalidraw/clients.ts::getNameInitial#Function",Function,48-54
      "packages/excalidraw/clients.ts::renderRemoteCursors#Function",Function,56-258
  - path: packages/excalidraw/clipboard.test.ts
    language: typescript
    line_count: 159
    symbols[1,]{id,symbolKind,line_span}:
      "packages/excalidraw/clipboard.test.ts::describe callback#Function",Function,9-158
  - path: packages/excalidraw/clipboard.ts
    language: typescript
    line_count: 692
    symbols[28,]{id,symbolKind,line_span}:
      "packages/excalidraw/clipboard.ts::ElementsClipboard#TypeAlias",TypeAlias,39-43
      "packages/excalidraw/clipboard.ts::PastedMixedContent#TypeAlias",TypeAlias,45-
      "packages/excalidraw/clipboard.ts::ClipboardData#Interface",Interface,47-54
      "packages/excalidraw/clipboard.ts::AllowedPasteMimeTypes#TypeAlias",TypeAlias,56-
      "packages/excalidraw/clipboard.ts::ParsedClipboardEventTextData#TypeAlias",TypeAlias,58-60
      "packages/excalidraw/clipboard.ts::clipboardContainsElements#Function",Function,74-88
      "packages/excalidraw/clipboard.ts::createPasteEvent#Function",Function,90-141
      "packages/excalidraw/clipboard.ts::serializeAsClipboardJSON#Function",Function,143-193
      "packages/excalidraw/clipboard.ts::copyToClipboard#Function",Function,195-210
      "packages/excalidraw/clipboard.ts::parseHTMLTree#Function",Function,213-231
      "packages/excalidraw/clipboard.ts::maybeParseHTMLDataItem#Function",Function,233-251
      "packages/excalidraw/clipboard.ts::readSystemClipboard#Function",Function,257-326
      "packages/excalidraw/clipboard.ts::parseClipboardEventTextData#Function",Function,331-3
```

## 4. `list_files`

```
{'path': 'packages/element', 'progress': 15}
```
**result**
```
dir: packages/element
subdirs[2,]{name,files}:
  src,53
  tests,25
files[1,]{path,language,line_count,docstring}:
  packages/element/global.d.ts,typescript,4,"<reference types=\"vite/client\" />"
```

## 5. `list_files`

```
{'path': 'packages/excalidraw/renderer', 'progress': 25}
```
**result**
```
dir: packages/excalidraw/renderer
subdirs[0]:
files[9]:
  - path: packages/excalidraw/renderer/animation.ts
    language: typescript
    line_count: 167
    symbols[3,]{id,symbolKind,line_span}:
      "packages/excalidraw/renderer/animation.ts::Animation#TypeAlias",TypeAlias,3-6
      "packages/excalidraw/renderer/animation.ts::AnimationRecord#TypeAlias",TypeAlias,8-12
      "packages/excalidraw/renderer/animation.ts::AnimationController#Class",Class,14-166
  - path: packages/excalidraw/renderer/helpers.test.ts
    language: typescript
    line_count: 91
    symbols[3,]{id,symbolKind,line_span}:
      "packages/excalidraw/renderer/helpers.test.ts::setup#Function",Function,5-13
      "packages/excalidraw/renderer/helpers.test.ts::run#Function",Function,15-25
      "packages/excalidraw/renderer/helpers.test.ts::describe callback#Function",Function,27-90
  - path: packages/excalidraw/renderer/helpers.ts
    language: typescript
    line_count: 158
    symbols[6,]{id,symbolKind,line_span}:
      "packages/excalidraw/renderer/helpers.ts::getSelectionColor#Function",Function,13-16
      "packages/excalidraw/renderer/helpers.ts::fillCircle#Function",Function,18-34
      "packages/excalidraw/renderer/helpers.ts::snapScrollToDevicePixels#Function",Function,47-63
      "packages/excalidraw/renderer/helpers.ts::getNormalizedCanvasDimensions#Function",Function,65-71
      "packages/excalidraw/renderer/helpers.ts::bootstrapCanvas#Function",Function,73-127
      "packages/excalidraw/renderer/helpers.ts::strokeRectWithRotation_simple#Function",Function,129-157
    constants[1]: DEFAULT_SELECTION_COLOR
  - path: packages/excalidraw/renderer/interactiveScene.ts
    language: typescript
    line_count: 2174
    symbols[23,]{id,symbolKind,line_span}:
      "packages/excalidraw/renderer/interactiveScene.ts::getThemedColor#Function",Function,145-148
      "packages/excalidraw/renderer/interactiveScene.ts::renderElbowArrowMidPointHighlight#Function",Function,150-161
      "packages/excalidraw/renderer/interactiveScene.ts::renderLinearElementPointHighlight#Function",Function,163-191
      "packages/excalidraw/renderer/interactiveScene.ts::highlightPoint#Function",Function,194-216
      "packages/excalidraw/renderer/interactiveScene.ts::renderHoveredArrowTextAnchor#Function",Function,228-251
      "packages/excalidraw/renderer/interactiveScene.ts::renderSingleLinearPoint#Function",Function,253-290
      "packages/excalidraw/renderer/interactiveScene.ts::renderBindingHighlightForBindableElement_simple#Function",Function,292-615
      "packages/excalidraw/renderer/interactiveScene.ts::renderBindingHighlightForBindableElement_complex#Function",Function,617-949
      "packages/excalidraw/renderer/interactiveScene.ts::renderBindingHighlightForBindableElement#Function",Function,951-996
      "packages/excalidraw/renderer/interactiveScene.ts::ElementSelectionBorder#TypeAlias",TypeAlias,998-1010
      "packages/excalidraw/renderer/interactiveScene.ts::renderSelectionBorder#Function",Function,1012-1065
      "packages/excalidraw/renderer/interactiveScene.ts::renderFrameHighlight#Function",Function,1067-1095
      "packages/excalidraw/renderer/interactiveScene.ts::renderElementsBoxHighlight#Function",Function,1097-1146
      "packages/excalidraw/renderer/interactiveScene.ts::renderLinearPointHandles#Function",Function,1148-1271
      "packages/excalidraw/renderer/interactiveScene.ts::renderFocusPointConnectionLine#Function",Function,1273-1295
      "packages/excalidraw/renderer/interactiveScene.ts::renderFocusPointCicle#Function",Function,1297-1326
      "packages/excalidraw/renderer/interactiveScene.ts::renderFocusPointIndicator#Function",Function,1328-1418
      "packages/excalidraw/renderer/interactiveScene.ts::renderTransformHandles#Function",Function,1420-1461
      "packages/excalidraw/renderer/interactiveScene.ts::renderCropHandles#Function",Function,1463-1566
      "packages/excalidraw/renderer/interactiveScene.ts::renderTextBox#Function",Function,1568
```

## 6. `list_files`

```
{'path': 'packages/excalidraw/scene', 'progress': 25}
```
**result**
```
dir: packages/excalidraw/scene
subdirs[0]:
files[6]:
  - path: packages/excalidraw/scene/export.ts
    language: typescript
    line_count: 588
    symbols[11,]{id,symbolKind,line_span}:
      "packages/excalidraw/scene/export.ts::truncateText#Function",Function,65-97
      "packages/excalidraw/scene/export.ts::addFrameLabelsAsTextElements#Function",Function,105-135
      "packages/excalidraw/scene/export.ts::getFrameRenderingConfig#Function",Function,137-148
      "packages/excalidraw/scene/export.ts::prepareElementsForRender#Function",Function,150-178
      "packages/excalidraw/scene/export.ts::exportToCanvas#Function",Function,180-284
      "packages/excalidraw/scene/export.ts::createHTMLComment#Function",Function,286-291
      "packages/excalidraw/scene/export.ts::exportToSvg#Function",Function,293-508
      "packages/excalidraw/scene/export.ts::encodeSvgBase64Payload#Function",Function,510-529
      "packages/excalidraw/scene/export.ts::decodeSvgBase64Payload#Function",Function,531-563
      "packages/excalidraw/scene/export.ts::getCanvasSize#Function",Function,566-575
      "packages/excalidraw/scene/export.ts::getExportSize#Function",Function,577-587
  - path: packages/excalidraw/scene/index.ts
    language: typescript
    line_count: 21
  - path: packages/excalidraw/scene/normalize.ts
    language: typescript
    line_count: 18
    symbols[3,]{id,symbolKind,line_span}:
      "packages/excalidraw/scene/normalize.ts::getNormalizedZoom#Function",Function,7-9
      "packages/excalidraw/scene/normalize.ts::getNormalizedGridSize#Function",Function,11-13
      "packages/excalidraw/scene/normalize.ts::getNormalizedGridStep#Function",Function,15-17
  - path: packages/excalidraw/scene/Renderer.ts
    language: typescript
    line_count: 263
    symbols[2,]{id,symbolKind,line_span}:
      "packages/excalidraw/scene/Renderer.ts::GetRenderableElementsOpts#TypeAlias",TypeAlias,25-38
      "packages/excalidraw/scene/Renderer.ts::Renderer#Class",Class,40-262
  - path: packages/excalidraw/scene/scrollbars.ts
    language: typescript
    line_count: 156
    symbols[2,]{id,symbolKind,line_span}:
      "packages/excalidraw/scene/scrollbars.ts::getScrollBars#Function",Function,15-130
      "packages/excalidraw/scene/scrollbars.ts::isOverScrollBars#Function",Function,132-155
    constants[3]: SCROLLBAR_COLOR,SCROLLBAR_MARGIN,SCROLLBAR_WIDTH
  - path: packages/excalidraw/scene/types.ts
    language: typescript
    line_count: 177
    symbols[15,]{id,symbolKind,line_span}:
      "packages/excalidraw/scene/types.ts::RenderableElementsMap#TypeAlias",TypeAlias,24-25
      "packages/excalidraw/scene/types.ts::StaticCanvasRenderConfig#TypeAlias",TypeAlias,27-43
      "packages/excalidraw/scene/types.ts::SVGRenderConfig#TypeAlias",TypeAlias,45-62
      "packages/excalidraw/scene/types.ts::InteractiveCanvasRenderConfig#TypeAlias",TypeAlias,64-77
      "packages/excalidraw/scene/types.ts::RenderInteractiveSceneCallback#TypeAlias",TypeAlias,79-81
      "packages/excalidraw/scene/types.ts::StaticSceneRenderConfig#TypeAlias",TypeAlias,83-92
      "packages/excalidraw/scene/types.ts::InteractiveSceneRenderAnimationState#TypeAlias",TypeAlias,94-96
      "packages/excalidraw/scene/types.ts::InteractiveSceneRenderConfig#TypeAlias",TypeAlias,98-112
      "packages/excalidraw/scene/types.ts::NewElementSceneRenderConfig#TypeAlias",TypeAlias,114-123
      "packages/excalidraw/scene/types.ts::SceneScroll#TypeAlias",TypeAlias,125-128
      "packages/excalidraw/scene/types.ts::ExportType#TypeAlias",TypeAlias,130-135
      "packages/excalidraw/scene/types.ts::ScrollBars#TypeAlias",TypeAlias,137-152
      "packages/excalidraw/scene/types.ts::SVGPathString#TypeAlias",TypeAlias,154-
      "packages/excalidraw/scene/types.ts::ElementShape#TypeAlias",TypeAlias,156-161
      "packages/excalidraw/scene/types.ts::ElementShapes#TypeAlias",TypeAlias,163-176
```

## 7. `list_files`

```
{'path': 'packages/element/src', 'progress': 30}
```
**result**
```
dir: packages/element/src
subdirs[2,]{name,files}:
  __tests__,1
  arrows,2
files[50]:
  - path: packages/element/src/align.ts
    language: typescript
    line_count: 83
    symbols[3,]{id,symbolKind,line_span}:
      "packages/element/src/align.ts::Alignment#Interface",Interface,14-17
      "packages/element/src/align.ts::alignElements#Function",Function,19-52
      "packages/element/src/align.ts::calculateTranslation#Function",Function,54-82
  - path: packages/element/src/arrowEndpointText.ts
    language: typescript
    line_count: 289
    docstring: "Text bound to an arrow endpoint — creating a text element that reads as a label for the tip of an arrow, placed and anchored so the arrow itself never moves."
    symbols[5,]{id,symbolKind,line_span}:
      "packages/element/src/arrowEndpointText.ts::ArrowEndpoint#TypeAlias",TypeAlias,51-54
      "packages/element/src/arrowEndpointText.ts::getUnboundArrowEndpointAtPoint#Function",Function,61-121
      "packages/element/src/arrowEndpointText.ts::getTextBindingForArrowEndpoint#Function",Function,133-252
      "packages/element/src/arrowEndpointText.ts::isEndpointBoundText#Function",Function,260-276
      "packages/element/src/arrowEndpointText.ts::getEndpointBoundTextDragAnchor#Function",Function,279-288
  - path: packages/element/src/arrowheads.ts
    language: typescript
    line_count: 33
    symbols[2,]{id,symbolKind,line_span}:
      "packages/element/src/arrowheads.ts::normalizeArrowhead#Function",Function,3-21
      "packages/element/src/arrowheads.ts::getArrowheadForPicker#Function",Function,23-32
  - path: packages/element/src/binding.ts
    language: typescript
    line_count: 3199
    symbols[57,]{id,symbolKind,line_span}:
      "packages/element/src/binding.ts::BindingStrategy#TypeAlias",TypeAlias,91-109
      "packages/element/src/binding.ts::getBindingGap#Function",Function,125-135
      "packages/element/src/binding.ts::maxBindingDistance_simple#Function",Function,137-147
      "packages/element/src/binding.ts::isBindingEnabled#Function",Function,149-153
      "packages/element/src/binding.ts::bindOrUnbindBindingElement#Function",Function,155-240
      "packages/element/src/binding.ts::bindOrUnbindBindingElementEdge#Function",Function,242-265
      "packages/element/src/binding.ts::bindingStrategyForElbowArrowEndpointDragging#Function",Function,267-317
      "packages/element/src/binding.ts::bindingStrategyForNewSimpleArrowEndpointDragging#Function",Function,319-475
      "packages/element/src/binding.ts::bindingStrategyForSimpleArrowEndpointDragging_complex#Function",Function,477-601
      "packages/element/src/binding.ts::getBindingStrategyForDraggingBindingElementEndpoints#Function",Function,603-642
      "packages/element/src/binding.ts::getBindingStrategyForDraggingBindingElementEndpoints_simple#Function",Function,644-953
      "packages/element/src/binding.ts::getBindingStrategyForDraggingBindingElementEndpoints_complex#Function",Function,955-1084
      "packages/element/src/binding.ts::bindOrUnbindBindingElements#Function",Function,1086-1101
      "packages/element/src/binding.ts::applyBinding#Function",Function,1107-1127
      "packages/element/src/binding.ts::bindBindingElement#Function",Function,1129-1171
      "packages/element/src/binding.ts::unbindBindingElement#Function",Function,1173-1203
      "packages/element/src/binding.ts::updateBoundElements#Function",Function,1207-1314
      "packages/element/src/binding.ts::updateArrowBindings#Function",Function,1316-1378
      "packages/element/src/binding.ts::updateBindings#Function",Function,1380-1417
      "packages/element/src/binding.ts::doesNeedUpdate#Function",Function,1419-1427
      "packages/element/src/binding.ts::getSimultaneouslyUpdatedElementIds#Function",Function,1429-1433
      "packages/element/src/binding.ts::getHeadingForElbowArrowSnap#Function",Function,1435-1464
      "packages/element/src/binding.ts::getDistanceForBinding#Function",Function,1466-1476
      "packages/element/src/bindin
```

## 8. `get_callers`

```
{'name_or_id': 'packages/excalidraw/renderer/staticScene.ts::renderStaticScene#Function', 'progress': 30}
```
**result**
```
target:
  id: "packages/excalidraw/renderer/staticScene.ts::renderStaticScene#Function"
  label: renderStaticScene
  symbolKind: Function
  path: packages/excalidraw/renderer/staticScene.ts
  line_span: 528-538
  called_by: 2
  refs: 0
callers[2,]{id,label,symbolKind,path,line_span,called_by,refs}:
  "packages/excalidraw/scene/export.ts::exportToCanvas#Function",exportToCanvas,Function,packages/excalidraw/scene/export.ts,180-284,2,0
  "packages/excalidraw/components/canvases/StaticCanvas.tsx::StaticCanvas#Function.useEffect callback#Function",useEffect callback,Function,packages/excalidraw/components/canvases/StaticCanvas.tsx,44-72,0,0
```

## 9. `profile`

```
{'name_or_id': 'packages/excalidraw/scene/Renderer.ts::Renderer#Class', 'progress': 30}
```
**result**
```
symbol:
  id: "packages/excalidraw/scene/Renderer.ts::Renderer#Class"
  symbolKind: Class
  line: 40
does:
  defines[2]: scene,_getRenderableElements
affects:
  callers[2]: App#Class.constructor#Method,App#Class.componentWillUnmount#Method
more: outline for the line-by-line body; trace_value_origin for full value origins; read_source for exact text
```

## 10. `skim_source`

```
{'name_or_id': 'packages/excalidraw/renderer/staticScene.ts::_renderStaticScene#Function', 'progress': 40}
```
**result**
```
{"id": "packages/excalidraw/renderer/staticScene.ts::_renderStaticScene#Function", "label": "_renderStaticScene", "symbolKind": "Function", "path": "packages/excalidraw/renderer/staticScene.ts", "line_span": "261-516", "called_by": 2, "refs": 0, "members": [{"id": "packages/excalidraw/renderer/staticScene.ts::_renderStaticScene#Function.forEach callback#Function", "label": "forEach callback", "symbolKind": "Function", "path": "packages/excalidraw/renderer/staticScene.ts", "line_span": "501-515", "called_by": 0, "refs": 0}, {"id": "packages/excalidraw/renderer/staticScene.ts::_renderStaticScene#Function.visibleElements callback#Function", "label": "visibleElements callback", "symbolKind": "Function", "path": "packages/excalidraw/renderer/staticScene.ts", "line_span": "427-498", "called_by": 0, "refs": 0}]}
--- skim ---
271 if (canvas === null)
272   return;
275 renderGrid = renderConfig
275 isExporting = renderConfig
277 appState = isExporting ? unsnappedAppState : snapScrollToDevicePixels(unsnappedAppState, scale)
279   snapScrollToDevicePixels#Function(unsnappedAppState, scale)  [rslvd]
281 normalizedWidth = getNormalizedCanvasDimensions( canvas, scale, )  [rslvd]
281 normalizedHeight = getNormalizedCanvasDimensions( canvas, scale, )  [rslvd]
286 context = bootstrapCanvas({ canvas, scale, normalizedWidth, normalizedHeight, theme: appState.theme, isExporti...  [rslvd]
297 context.scale(appState.zoom.value, appState.zoom.value)  [unrslvd: untyped_local]
300 if (renderGrid)
301   strokeGrid#Function(context, appState.gridSize, appState.gridStep, appState.scrollX, appState.scrollY, appState.zoom, renderConfig.theme, n…)  [rslvd]
315 groupsToBeAddedToFrame = new Set<string>()  [extrn]
317 visibleElements.forEach((element) => { if ( element.groupIds.length > 0 && appState…)  [unrslvd: untyped_local]
335 inFrameGroupsMap = new Map<string, boolean>()  [extrn]
338 forEach((element) => { try { const frameId = element.frameId || app…)  [unrslvd: opaque_receiver]
338 visibleElements.filter((el) => !isIframeLikeElement(el))  [unrslvd: untyped_local]
501 renderConfig.pendingFlowchartNodes.forEach((element) => { try { renderElement( element, elementsMap, a…)  [unrslvd: untyped_local]
```

## 11. `get_definition`

```
{'name_or_id': 'packages/excalidraw/components/canvases/StaticCanvas.tsx::StaticCanvas#Function', 'progress': 40}
```
**result**
```
id: "packages/excalidraw/components/canvases/StaticCanvas.tsx::StaticCanvas#Function"
label: StaticCanvas
symbolKind: Function
path: packages/excalidraw/components/canvases/StaticCanvas.tsx
line_span: 33-75
called_by: 0
refs: 1
parent: "packages/excalidraw/components/canvases/StaticCanvas.tsx::<module>"
children[1,]{id,label,symbolKind,path,line_span,called_by,refs}:
  "packages/excalidraw/components/canvases/StaticCanvas.tsx::StaticCanvas#Function.useEffect callback#Function",useEffect callback,Function,packages/excalidraw/components/canvases/StaticCanvas.tsx,44-72,0,0
parameters[1]: props
signature: "(props: StaticCanvasProps)"
referenced_by[1]:
  - scope: "packages/excalidraw/components/canvases/index.tsx::<module>"
    kind: name
    lines[1]: 4
```

## 12. `profile`

```
{'name_or_id': 'packages/element/src/Scene.ts::Scene#Class', 'progress': 40}
```
**result**
```
symbol:
  id: "packages/element/src/Scene.ts::Scene#Class"
  symbolKind: Class
  line: 108
does:
  defines[9]: callbacks,nonDeletedElements,nonDeletedElementsMap,elements,nonDeletedFramesLikes,frames,elementsMap,selectedElementsCache,sceneNonce
affects:
  callers[5]: App#Class.constructor#Method,App#Class.componentWillUnmount#Method,ElementsDelta#Class.redrawElements#Method,convertToExcalidrawElements#Function,describe callback#Function.it callback#Function
more: outline for the line-by-line body; trace_value_origin for full value origins; read_source for exact text
```

## 13. `skim_source`

```
{'name_or_id': 'packages/element/src/mutateElement.ts::mutateElement#Function', 'progress': 40}
```
**result**
```
{"id": "packages/element/src/mutateElement.ts::mutateElement#Function", "label": "mutateElement", "symbolKind": "Function", "path": "packages/element/src/mutateElement.ts", "line_span": "40-147", "called_by": 20, "refs": 1}
--- skim ---
50 didChange = false
54 points = updates as any
54 fixedSegments = updates as any
54 fileId = updates as any
56 if (
57   isElbowArrow#Function(element)  [rslvd]
58   Object.keys(updates)  [extrn]
62   updates = { ...updates, angle: 0 as Radians, ...updateElbowArrowPoints( { ...(element as ExcalidrawElbowArrowE...
65     updateElbowArrowPoints#Function({ ...(element as ExcalidrawElbowArrowElement), x: updates.x…, elementsMap as NonDeletedSceneElementsMap, updates as Ele…)  [rslvd]
76 if (typeof points !== "undefined")
77   updates = { ...getSizeFromPoints(points), ...updates }  [rslvd]
80 for (const key in updates)
81   value = (updates as any)[key]
82   if (typeof value !== "undefined")
83     if (
92       continue;
95     if (key === "scale")
96       prevScale = (element as any)[key]
97       nextScale = value
98       if (prevScale[0] === nextScale[0] && prevScale[1] === nextScale[1])
99         continue;
101     if (key === "points")
102       prevPoints = (element as any)[key]
103       nextPoints = value
104       if (prevPoints.length === nextPoints.length)
105         didChangePoints = false
106         index = prevPoints.length
107         index += 
107         while (--index)
108           prevPoint = prevPoints[index]
109           nextPoint = nextPoints[index]
110           if (
114             didChangePoints = true
115             break;
118         if (!didChangePoints)
119           continue;
124     (element as any)[key] = value
125     didChange = true
129 if (!didChange)
130   return element;
[steps 1-40 of 46 -- call again with offset=40 for the next page]
```

## 14. `skim_source`

```
{'name_or_id': 'packages/element/src/mutateElement.ts::mutateElement#Function', 'offset': 40, 'progress': 55}
```
**result**
```
{"id": "packages/element/src/mutateElement.ts::mutateElement#Function", "label": "mutateElement", "symbolKind": "Function", "path": "packages/element/src/mutateElement.ts", "line_span": "40-147", "called_by": 20, "refs": 1}
--- skim ---
133 if (
139   ShapeCache#Class.delete#Function(element)  [rslvd]
142 element.version = updates.version ?? element.version + 1
143 element.versionNonce = updates.versionNonce ?? randomInteger()  [rslvd]
144 element.updated = getUpdatedTimestamp()  [rslvd]
146 return element;
[steps 41-46 of 46]
```

## 15. `search_symbols`

```
{'query': ['triggerRender', 'informMutation', 'onUpdate'], 'progress': 55}
```
**result**
```
triggerRender[1,]{id,label,symbolKind,path,line_span,called_by,refs}:
  "packages/excalidraw/components/App.tsx::App#Class.triggerRender#Function",triggerRender,Function,packages/excalidraw/components/App.tsx,5338-5347,5,0
informMutation[0]:
onUpdate[4]:
  - id: "packages/element/src/Scene.ts::Scene#Class.onUpdate#Method"
    label: onUpdate
    symbolKind: Method
    path: packages/element/src/Scene.ts
    line_span: 311-324
    called_by: 1
    refs: 0
  - id: "packages/excalidraw/wysiwyg/textWysiwyg.tsx::textWysiwyg#Function.onUpdate callback#Function"
    label: onUpdate callback
    symbolKind: Function
    path: packages/excalidraw/wysiwyg/textWysiwyg.tsx
    line_span: 985-993
    called_by: 0
    refs: 0
  - id: "packages/element/src/types.ts::PointsPositionUpdates#TypeAlias"
    label: PointsPositionUpdates
    symbolKind: TypeAlias
    path: packages/element/src/types.ts
    line_span: 313-316
    called_by: 0
    refs: 2
  - id: "packages/excalidraw/actions/actionFrame.ts::actionupdateFrameRendering"
    label: actionupdateFrameRendering
    symbolKind: Binding
    scope: "packages/excalidraw/actions/actionFrame.ts::<module>"
    line: 104
    value: "register({ name: \"updateFrameRendering\", label: \"labels.upda"
```

## 16. `read_source`

```
{'name_or_id': 'packages/excalidraw/components/canvases/StaticCanvas.tsx', 'start_line': 33, 'end_line': 75, 'progress': 55}
```
**result**
```
{"id": "packages/excalidraw/components/canvases/StaticCanvas.tsx::<module>", "label": "StaticCanvas.tsx", "symbolKind": "Module", "path": "packages/excalidraw/components/canvases/StaticCanvas.tsx", "line_span": "1-135", "called_by": 0, "refs": 0, "start_line": 33, "end_line": 75}
--- source ---
const StaticCanvas = (props: StaticCanvasProps) => {
  const wrapperRef = useRef<HTMLDivElement>(null);
  const isComponentMounted = useRef(false);

  useEffect(() => {
    props.canvas.style.width = `${props.appState.width}px`;
    props.canvas.style.height = `${props.appState.height}px`;
    props.canvas.width = props.appState.width * props.scale;
    props.canvas.height = props.appState.height * props.scale;
  }, [props.appState.height, props.appState.width, props.canvas, props.scale]);

  useEffect(() => {
    const wrapper = wrapperRef.current;
    if (!wrapper) {
      return;
    }

    const canvas = props.canvas;

    if (!isComponentMounted.current) {
      isComponentMounted.current = true;

      wrapper.replaceChildren(canvas);
      canvas.classList.add("excalidraw__canvas", "static");
    }

    renderStaticScene(
      {
        canvas,
        rc: props.rc,
        scale: props.scale,
        elementsMap: props.elementsMap,
        allElementsMap: props.allElementsMap,
        visibleElements: props.visibleElements,
        appState: props.appState,
        renderConfig: props.renderConfig,
      },
      isRenderThrottlingEnabled(),
    );
  });

  return <div className="excalidraw__canvas-wrapper" ref={wrapperRef} />;
};
```

## 17. `skim_source`

```
{'name_or_id': 'packages/element/src/renderElement.ts::renderElement#Function', 'progress': 65}
```
**result**
```
{"id": "packages/element/src/renderElement.ts::renderElement#Function", "label": "renderElement", "symbolKind": "Function", "path": "packages/element/src/renderElement.ts", "line_span": "810-1081", "called_by": 4, "refs": 0}
--- skim ---
819   reduceAlphaForSelection = appState.openDialog?.name === "elementLinkSelector" && !appState.selectedElementIds[element.id] && !...
824   context.globalAlpha = getRenderOpacity( element, getContainingFrame(element, elementsMap), renderCon...  [rslvd]
826     getContainingFrame#Function(element, elementsMap)  [rslvd]
832   switch (element.type)
833     case "magicframe":
834     case "frame":
835       if (appState.frameRendering.enabled && appState.frameRendering.outline)
836         context.save()  [unrslvd: untyped_local]
837         context.translate(element.x + appState.scrollX, element.y + appState.scrollY)  [unrslvd: untyped_local]
841         context.fillStyle = "rgba(0, 0, 200, 0.04)"
843         context.lineWidth = FRAME_STYLE.strokeWidth / appState.zoom.value
844         context.strokeStyle = applyDarkModeFilter( FRAME_STYLE.strokeColor, appState.theme === THEME.DARK, )  [rslvd]
850         if (isMagicFrameElement(element))  [rslvd]
851           context.strokeStyle = appState.theme === THEME.LIGHT ? "#7affd7" : applyDarkModeFilter("#1d8264")
857         if (FRAME_STYLE.radius && context.roundRect)
858           context.beginPath()  [unrslvd: untyped_local]
859           context.roundRect(0, 0, element.width, element.height, FRAME_STYLE.radius / appState.zoom.value)  [unrslvd: untyped_local]
866           context.stroke()  [unrslvd: untyped_local]
867           context.closePath()  [unrslvd: untyped_local]
869           context.strokeRect(0, 0, element.width, element.height)  [unrslvd: untyped_local]
872         context.restore()  [unrslvd: untyped_local]
874       break;
876     case "freedraw":
877       if (renderConfig.isExporting)
878         x1 = getElementAbsoluteCoords(element, elementsMap)  [rslvd]
878         y1 = getElementAbsoluteCoords(element, elementsMap)  [rslvd]
878         x2 = getElementAbsoluteCoords(element, elementsMap)  [rslvd]
878         y2 = getElementAbsoluteCoords(element, elementsMap)  [rslvd]
879         cx = (x1 + x2) / 2 + appState.scrollX
880         cy = (y1 + y2) / 2 + appState.scrollY
881         shiftX = (x2 - x1) / 2 - (element.x - x1)
882         shiftY = (y2 - y1) / 2 - (element.y - y1)
885         context.rotate(element.angle)  [unrslvd: untyped_local]
887         drawElementOnCanvas#Function(element, rc, context, renderConfig)  [rslvd]
890         elementWithCanvas = generateElementWithCanvas( element, allElementsMap, renderConfig, appState, )  [rslvd]
896         if (!elementWithCanvas)
897           return;
900         drawElementFromCanvas#Function(elementWithCanvas, context, renderConfig, appState, allElementsMap)  [rslvd]
909       break;
911     case "rectangle":
[steps 1-40 of 100 -- call again with offset=40 for the next page]
```

## 18. `search_symbols`

```
{'query': ['ShapeCache'], 'progress': 65}
```
**result**
```
ShapeCache[2,]{id,label,symbolKind,path,line_span,called_by,refs}:
  "packages/element/src/shape.ts::ShapeCache#Class",ShapeCache,Class,packages/element/src/shape.ts,82-165,0,0
  "packages/excalidraw/components/App.tsx::App#Class.clearImageShapeCache#Method",clearImageShapeCache,Method,packages/excalidraw/components/App.tsx,3703-3711,2,0
```

## 19. `get_definition`

```
{'name_or_id': 'packages/element/src/Scene.ts::Scene#Class.onUpdate#Method', 'progress': 65}
```
**result**
```
id: "packages/element/src/Scene.ts::Scene#Class.onUpdate#Method"
label: onUpdate
symbolKind: Method
path: packages/element/src/Scene.ts
line_span: 311-324
called_by: 1
refs: 0
parent: "packages/element/src/Scene.ts::Scene#Class"
children[1,]{id,label,symbolKind,path,line_span,called_by,refs}:
  "packages/element/src/Scene.ts::Scene#Class.onUpdate#Method.<anonymous>#Function",<anonymous>,Function,packages/element/src/Scene.ts,318-323,0,0
parameters[1]: cb
signature: "(cb: SceneStateCallback)"
returns: SceneStateCallbackRemover
```

## 20. `skim_source`

```
{'name_or_id': 'packages/element/src/shape.ts::ShapeCache#Class', 'progress': 75}
```
**result**
```
{"id": "packages/element/src/shape.ts::ShapeCache#Class", "label": "ShapeCache", "symbolKind": "Class", "path": "packages/element/src/shape.ts", "line_span": "82-165", "called_by": 0, "refs": 0, "members": [{"id": "packages/element/src/shape.ts::ShapeCache#Class.get#Function", "label": "get", "symbolKind": "Function", "path": "packages/element/src/shape.ts", "line_span": "93-104", "called_by": 2, "refs": 0}, {"id": "packages/element/src/shape.ts::ShapeCache#Class.delete#Function", "label": "delete", "symbolKind": "Function", "path": "packages/element/src/shape.ts", "line_span": "106-109", "called_by": 9, "refs": 0}, {"id": "packages/element/src/shape.ts::ShapeCache#Class.destroy#Function", "label": "destroy", "symbolKind": "Function", "path": "packages/element/src/shape.ts", "line_span": "111-113", "called_by": 1, "refs": 0}, {"id": "packages/element/src/shape.ts::ShapeCache#Class.generateElementShape#Function", "label": "generateElementShape", "symbolKind": "Function", "path": "packages/element/src/shape.ts", "line_span": "119-164", "called_by": 4, "refs": 0}]}
--- skim ---
83 rg = new RoughGenerator()
84 cache = new WeakMap< ExcalidrawElement, { shape: ElementShape; theme: AppState["theme"] } >()
```

## 21. `search_symbols`

```
{'query': ['triggerUpdate'], 'progress': 75}
```
**result**
```
triggerUpdate[1,]{id,label,symbolKind,path,line_span,called_by,refs}:
  "packages/element/src/Scene.ts::Scene#Class.triggerUpdate#Method",triggerUpdate,Method,packages/element/src/Scene.ts,303-309,7,0
```

## Final answer

I now have a complete enough picture of the rendering pipeline. Here's the architecture:

## TL;DR

Excalidraw renders with **layered HTML canvases**, draws shapes via **Rough.js** (cached per-element), and re-renders through a **React effect loop driven by a `Scene` model**: a data mutation bumps the element's version → `Scene.triggerUpdate()` notifies subscribers → `App` re-renders → canvas components' `useEffect` (which runs on every render, no dep array) calls a **throttled, RAF-scheduled** scene-render function that walks the element list and draws each one.

## The pipeline, step by step

**1. Data model — `ExcalidrawElement` + `Scene`**
- `Scene` (`packages/element/src/Scene.ts`) owns the authoritative element array/map, a `sceneNonce`, and a callback registry (`onUpdate`, called by `triggerUpdate`, 7 call sites — i.e. every mutation path funnels through it).
- Elements are updated via `mutateElement` (`packages/element/src/mutateElement.ts`): it diffs `updates` against the element's current fields, mutates in place for perf, and critically **bumps `element.version`/`versionNonce`** and calls `ShapeCache.delete(element)` when geometry-relevant fields changed — invalidating the cached Rough.js shape so it regenerates on next draw.

**2. Shape generation — Rough.js, cached**
- `ShapeCache` (`packages/element/src/shape.ts`) wraps a single `RoughGenerator` instance and a `WeakMap<ExcalidrawElement, {shape, theme}>` cache. `generateElementShape` builds the rough.js path/shape (rectangle, ellipse, freedraw outline, etc.) only once per element version; `ShapeCache.get` returns the cached shape otherwise. This is what makes re-renders cheap — unchanged elements skip Rough.js entirely.

**3. Two canvases, two renderers**
Excalidraw splits drawing across layered `<canvas>` elements:
- **Static canvas** (`packages/excalidraw/renderer/staticScene.ts`, `_renderStaticScene`/`renderStaticScene`) — draws the actual elements: grid, frames, and each visible element via `renderElement` (`packages/element/src/renderElement.ts`), which switches on `element.type` and either strokes/fills directly or composites a cached offscreen `elementWithCanvas` (for freedraw/filtered elements) onto the main context.
- **Interactive canvas** (`packages/excalidraw/renderer/interactiveScene.ts`, `_renderInteractiveScene`/`renderInteractiveScene`) — draws selection borders, transform/resize handles, binding highlights, focus points, crop handles — the UI chrome, kept separate so it can repaint without redrawing every element.
- Both entry points are **throttled via `throttleRAF`** (`renderStaticSceneThrottled`, `renderNewElementSceneThrottled`), so a burst of state updates collapses into one paint per frame.

**4. React wiring — `App` → `StaticCanvas`/`InteractiveCanvas`**
- `App.tsx` holds `Scene` and the `AppState`; `Renderer` (`packages/excalidraw/scene/Renderer.ts`) computes the renderable/visible element set from the scene for a given viewport.
- `StaticCanvas` (`packages/excalidraw/components/canvases/StaticCanvas.tsx`) is a function component whose `useEffect` has **no dependency array** — it runs after *every* React render of `App` — and calls `renderStaticScene(...)` with the current canvas/elements/appState/renderConfig. So any state change that causes `App` to re-render (via `setState`, often triggered by `App.triggerRender`, called from `Scene.onUpdate` subscribers or direct state setters) results in a repaint.
- `exportToCanvas` (`packages/excalidraw/scene/export.ts`) reuses the same `renderStaticScene` for PNG/canvas export, and `renderSceneToSvg` (`staticSvgScene.ts`) is the parallel SVG serialization path for export (re-walks elements, emits SVG nodes instead of canvas draws).

**5. The update loop in short**
```
user action / API call
  → mutateElement(element, updates)      // version bump, ShapeCache invalidated
  → Scene stores it, Scene.triggerUpdate()
  → subscribers (App) call triggerRender() → setState
  → App re-renders (React)
  → StaticCanvas/InteractiveCanvas useEffect fires (every render)
  → renderStaticScene / renderInteractiveScene (RAF-throttled)
  → per element: ShapeCache.get (regenerate via Rough.js if invalidated) → renderElement draws to canvas
```

This is inference from static structure (no traced run), but it's grounded directly in the call graph: `mutateElement` → `ShapeCache.delete`, `Scene.triggerUpdate` (7 callers), `StaticCanvas`'s dependency-less `useEffect` calling `renderStaticScene`, and `renderStaticScene`'s only two callers being that effect and `exportToCanvas`.
