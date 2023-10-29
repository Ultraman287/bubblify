import { Fragment, useContext, useEffect, useRef, useState } from "react"
import { useRouter } from "next/router"
import { Event, getAllLocalStorageItems, getRefValue, getRefValues, isTrue, preventDefault, refs, spreadArraysOrObjects, uploadFiles, useEventLoop } from "/utils/state"
import { ColorModeContext, EventLoopContext, initialEvents, StateContext } from "/utils/context.js"
import "focus-visible/dist/focus-visible"
import "katex/dist/katex.min.css"
import { Box, Code, Heading, HStack, Image, Link, ListItem, Menu, MenuButton, MenuDivider, MenuItem, MenuList, Modal, ModalBody, ModalContent, ModalHeader, ModalOverlay, OrderedList, Spacer, Text, UnorderedList, VStack } from "@chakra-ui/react"
import { getEventURL } from "/utils/state.js"
import NextLink from "next/link"
import ReactMarkdown from "react-markdown"
import remarkMath from "remark-math"
import remarkGfm from "remark-gfm"
import rehypeKatex from "rehype-katex"
import rehypeRaw from "rehype-raw"
import { Prism } from "react-syntax-highlighter"
import { light } from "/styles/code/prism"
import { HamburgerIcon } from "@chakra-ui/icons"
import NextHead from "next/head"



export default function Component() {
  const state = useContext(StateContext)
  const router = useRouter()
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)
  const focusRef = useRef();
  
  // Main event loop.
  const [addEvents, connectError] = useContext(EventLoopContext)

  // Set focus to the specified element.
  useEffect(() => {
    if (focusRef.current) {
      focusRef.current.focus();
    }
  })

  // Route after the initial page hydration.
  useEffect(() => {
    const change_complete = () => addEvents(initialEvents())
    router.events.on('routeChangeComplete', change_complete)
    return () => {
      router.events.off('routeChangeComplete', change_complete)
    }
  }, [router])


  return (
    <Fragment>
  <Fragment>
  {isTrue(connectError !== null) ? (
  <Fragment>
  <Modal isOpen={connectError !== null}>
  <ModalOverlay>
  <ModalContent>
  <ModalHeader>
  {`Connection Error`}
</ModalHeader>
  <ModalBody>
  <Text>
  {`Cannot connect to server: `}
  {(connectError !== null) ? connectError.message : ''}
  {`. Check if server is reachable at `}
  {getEventURL().href}
</Text>
</ModalBody>
</ModalContent>
</ModalOverlay>
</Modal>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  <HStack alignItems={`flex-start`} sx={{"transition": "left 0.5s, width 0.5s", "position": "relative"}}>
  <Box sx={{"display": "flex", "flexDirection": "column", "position": "fixed", "top": "1", "right": "0", "borderRight": "1px solid #F4F3F6"}}>
  <VStack sx={{"height": "100dvh"}}>
  <VStack alignItems={`flex-start`} sx={{"width": "100%", "overflowY": "auto", "padding": "1em"}}>
  <Link as={NextLink} href={`/`}>
  <HStack sx={{"bg": isTrue((state.router.page.path === "/home") || (((state.router.page.path === "/") && "Home") === "Home")) ? `#F5EFFE` : `transparent`, "color": isTrue((state.router.page.path === "/home") || (((state.router.page.path === "/") && "Home") === "Home")) ? `#1A1060` : `black`, "borderRadius": "50%", "boxShadow": "0px 0px 0px 1px rgba(84, 82, 95, 0.14)", "width": "70px", "height": "70px", "paddingX": "1em"}}>
  <Image src={`/github.svg`} sx={{"height": "2.5em", "padding": "0.5em"}}/>
</HStack>
</Link>
  <Link as={NextLink} href={`/add-cluster`}>
  <HStack sx={{"bg": isTrue((state.router.page.path === "/add cluster") || (((state.router.page.path === "/") && "Add Cluster") === "Home")) ? `#F5EFFE` : `transparent`, "color": isTrue((state.router.page.path === "/add cluster") || (((state.router.page.path === "/") && "Add Cluster") === "Home")) ? `#1A1060` : `black`, "borderRadius": "50%", "boxShadow": "0px 0px 0px 1px rgba(84, 82, 95, 0.14)", "width": "70px", "height": "70px", "paddingX": "1em"}}>
  <Image src={`/add_cluster.svg`} sx={{"height": "2.5em", "padding": "0.5em"}}/>
</HStack>
</Link>
  <Link as={NextLink} href={`/dashboard`}>
  <HStack sx={{"bg": isTrue((state.router.page.path === "/dashboard") || (((state.router.page.path === "/") && "Dashboard") === "Home")) ? `#F5EFFE` : `transparent`, "color": isTrue((state.router.page.path === "/dashboard") || (((state.router.page.path === "/") && "Dashboard") === "Home")) ? `#1A1060` : `black`, "borderRadius": "50%", "boxShadow": "0px 0px 0px 1px rgba(84, 82, 95, 0.14)", "width": "70px", "height": "70px", "paddingX": "1em"}}>
  <Image src={`/github.svg`} sx={{"height": "2.5em", "padding": "0.5em"}}/>
</HStack>
</Link>
  <Link as={NextLink} href={`/settings`}>
  <HStack sx={{"bg": isTrue((state.router.page.path === "/settings") || (((state.router.page.path === "/") && "Settings") === "Home")) ? `#F5EFFE` : `transparent`, "color": isTrue((state.router.page.path === "/settings") || (((state.router.page.path === "/") && "Settings") === "Home")) ? `#1A1060` : `black`, "borderRadius": "50%", "boxShadow": "0px 0px 0px 1px rgba(84, 82, 95, 0.14)", "width": "70px", "height": "70px", "paddingX": "1em"}}>
  <Image src={`/settings.svg`} sx={{"height": "2.5em", "padding": "0.5em"}}/>
</HStack>
</Link>
</VStack>
  <Spacer/>
</VStack>
</Box>
  <Box sx={{"paddingTop": "5em", "paddingX": ["auto", "2em"]}}>
  <Box sx={{"width": "100%", "alignItems": "flex-start", "boxShadow": "0px 0px 0px 1px rgba(84, 82, 95, 0.14)", "borderRadius": "0.375rem", "padding": "1em", "marginBottom": "2em"}}>
  <ReactMarkdown components={{"h1": ({children, ...props}) => <Heading as={`h1`} size={`2xl`} sx={{"marginY": "0.5em"}} {...props}>   {children} </Heading>, "h2": ({children, ...props}) => <Heading as={`h2`} size={`xl`} sx={{"marginY": "0.5em"}} {...props}>   {children} </Heading>, "h3": ({children, ...props}) => <Heading as={`h3`} size={`lg`} sx={{"marginY": "0.5em"}} {...props}>   {children} </Heading>, "h4": ({children, ...props}) => <Heading as={`h4`} size={`md`} sx={{"marginY": "0.5em"}} {...props}>   {children} </Heading>, "h5": ({children, ...props}) => <Heading as={`h5`} size={`sm`} sx={{"marginY": "0.5em"}} {...props}>   {children} </Heading>, "h6": ({children, ...props}) => <Heading as={`h6`} size={`xs`} sx={{"marginY": "0.5em"}} {...props}>   {children} </Heading>, "p": ({children, ...props}) => <Text sx={{"marginY": "1em"}} {...props}>   {children} </Text>, "ul": ({children, ...props}) => <UnorderedList sx={{"marginY": "1em"}} {...props}>   {children} </UnorderedList>, "ol": ({children, ...props}) => <OrderedList sx={{"marginY": "1em"}} {...props}>   {children} </OrderedList>, "li": ({children, ...props}) => <ListItem sx={{"marginY": "0.5em"}} {...props}>   {children} </ListItem>, "a": ({children, ...props}) => <Link as={``} sx={{"fontWeight": "bold", "color": "#03030B", "textDecoration": "underline", "textDecorationColor": "#AD9BF8", "_hover": {"color": "#AD9BF8", "textDecoration": "underline", "textDecorationColor": "#03030B"}}} {...props}>   {children} </Link>, "code": ({inline, className, children, ...props}) => {     const match = (className || '').match(/language-(?<lang>.*)/);     const language = match ? match[1] : '';     return inline ? (         <Code sx={{"color": "#1F1944", "bg": "#EAE4FD"}} {...props}>   {children} </Code>     ) : (         <Prism customStyle={{"marginY": "1em"}} language={language} style={light} sx={{"marginY": "1em"}} children={String(children)} {...props}/>     );       }, "codeblock": ({children, ...props}) => <Prism customStyle={{"marginY": "1em"}} style={light} sx={{"marginY": "1em"}} {...props}/>}} rehypePlugins={[rehypeKatex, rehypeRaw]} remarkPlugins={[remarkMath, remarkGfm]}>
  {`# bubblify
A web application to automatically cluster emails into customized bubbles.

# Welcome to Reflex!

This is the base Reflex template - installed when you run \`reflex init\`.

If you want to use a different template, pass the \`--template\` flag to \`reflex init\`.
For example, if you want a more basic starting point, you can run:

\`\`\`bash
reflex init --template blank
\`\`\`

## About this Template

This template has the following directory structure:

\`\`\`bash
├── README.md
├── assets
├── rxconfig.py
└── {your_app}
    ├── __init__.py
    ├── components
    │   ├── __init__.py
    │   └── sidebar.py
    ├── pages
    │   ├── __init__.py
    │   ├── dashboard.py
    │   ├── index.py
    │   └── settings.py
    ├── state.py
    ├── styles.py
    ├── templates
    │   ├── __init__.py
    │   └── template.py
    └── {your_app}.py
\`\`\`

See the [Project Structure docs](https://reflex.dev/docs/getting-started/project-structure/) for more information on general Reflex project structure.

### Adding Pages

In this template, the pages in your app are defined in \`{your_app}/pages/\`.
Each page is a function that returns a Reflex component.
For example, to edit this page you can modify \`{your_app}/pages/index.py\`.
See the [pages docs](https://reflex.dev/docs/components/pages/) for more information on pages.

In this template, instead of using \`rx.add_page\` or the \`@rx.page\` decorator,
we use the \`@template\` decorator from \`{your_app}/templates/template.py\`.

To add a new page:

1. Add a new file in \`{your_app}/pages/\`. We recommend using one file per page, but you can also group pages in a single file.
2. Add a new function with the \`@template\` decorator, which takes the same arguments as \`@rx.page\`.
3. Import the page in your \`{your_app}/pages/__init__.py\` file and it will automatically be added to the app.


### Adding Components

In order to keep your code organized, we recommend putting components that are
used across multiple pages in the \`{your_app}/components/\` directory.

In this template, we have a sidebar component in \`{your_app}/components/sidebar.py\`.

### Adding State

In this template, we define the base state of the app in \`{your_app}/state.py\`.
The base state is useful for general app state that is used across multiple pages.

In this template, the base state handles the toggle for the sidebar.

As your app grows, we recommend using [substates](https://reflex.dev/docs/state/substates/)
to organize your state. You can either define substates in their own files, or if the state is
specific to a page, you can define it in the page file itself.
`}
</ReactMarkdown>
</Box>
</Box>
  <Spacer/>
  <Box sx={{"position": "fixed", "right": "1.5em", "top": "1.5em", "zIndex": "500"}}>
  <Menu>
  <MenuButton sx={{"width": "3em", "height": "3em", "backgroundColor": "white", "border": "1px solid #F4F3F6", "borderRadius": "0.375rem"}}>
  <HamburgerIcon sx={{"size": "4em", "color": "black"}}/>
</MenuButton>
  <MenuList>
  <MenuItem sx={{"_hover": {"bg": "#F5EFFE"}}}>
  <Link as={NextLink} href={`/`} sx={{"width": "100%"}}>
  {`Home`}
</Link>
</MenuItem>
  <MenuItem sx={{"_hover": {"bg": "#F5EFFE"}}}>
  <Link as={NextLink} href={`/add-cluster`} sx={{"width": "100%"}}>
  {`Add Cluster`}
</Link>
</MenuItem>
  <MenuItem sx={{"_hover": {"bg": "#F5EFFE"}}}>
  <Link as={NextLink} href={`/dashboard`} sx={{"width": "100%"}}>
  {`Dashboard`}
</Link>
</MenuItem>
  <MenuItem sx={{"_hover": {"bg": "#F5EFFE"}}}>
  <Link as={NextLink} href={`/settings`} sx={{"width": "100%"}}>
  {`Settings`}
</Link>
</MenuItem>
  <MenuDivider/>
  <MenuItem sx={{"_hover": {"bg": "#F5EFFE"}}}>
  <Link as={NextLink} href={`https://github.com/reflex-dev`} sx={{"width": "100%"}}>
  {`About`}
</Link>
</MenuItem>
  <MenuItem sx={{"_hover": {"bg": "#F5EFFE"}}}>
  <Link as={NextLink} href={`mailto:founders@=reflex.dev`} sx={{"width": "100%"}}>
  {`Contact`}
</Link>
</MenuItem>
</MenuList>
</Menu>
</Box>
</HStack>
  <NextHead>
  <title>
  {`Home`}
</title>
  <meta content={`A Reflex app.`} name={`description`}/>
  <meta content={`/github.svg`} property={`og:image`}/>
  <meta content={`width=device-width, shrink-to-fit=no, initial-scale=1`} name={`viewport`}/>
</NextHead>
</Fragment>
  )
}
