import { Fragment, useContext, useEffect, useRef, useState } from "react"
import { useRouter } from "next/router"
import { Event, getAllLocalStorageItems, getRefValue, getRefValues, isTrue, preventDefault, refs, spreadArraysOrObjects, uploadFiles, useEventLoop } from "/utils/state"
import { ColorModeContext, EventLoopContext, initialEvents, StateContext } from "/utils/context.js"
import "focus-visible/dist/focus-visible"
import { Box, Code, Heading, HStack, Image, Link, Menu, MenuButton, MenuDivider, MenuItem, MenuList, Modal, ModalBody, ModalContent, ModalHeader, ModalOverlay, Spacer, Text, VStack } from "@chakra-ui/react"
import { getEventURL } from "/utils/state.js"
import NextLink from "next/link"
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
  <HStack alignItems={`flex-start`} sx={{"transition": "left 0.5s, width 0.5s", "position": "relative", "width": "100%", "height": "100%"}}>
  <Box sx={{"display": "flex", "flexDirection": "column", "position": "fixed", "right": "0", "bottom": "0"}}>
  <VStack>
  <VStack alignItems={`flex-start`} sx={{"width": "100%", "overflowY": "auto", "padding": "1em"}}>
  <Link as={NextLink} href={`/`}>
  <HStack sx={{"bg": isTrue((state.router.page.path === "/home") || (((state.router.page.path === "/") && "Home") === "Home") || ((state.router.page.path === "/add-cluster") && false)) ? `#F5EFFE` : `transparent`, "color": isTrue((state.router.page.path === "/home") || (((state.router.page.path === "/") && "Home") === "Home") || ((state.router.page.path === "/add-cluster") && false)) ? `#1A1060` : `black`, "borderRadius": "50%", "boxShadow": "0px 0px 0px 1px rgba(84, 82, 95, 0.14)", "width": "80px", "height": "80px", "padding": "0.9em", "margin": "0.5em"}}>
  <Image src={`/home.svg`} sx={{"padding": "0.5em"}}/>
</HStack>
</Link>
  <Link as={NextLink} href={`/add-cluster`}>
  <HStack sx={{"bg": isTrue((state.router.page.path === "/add cluster") || (((state.router.page.path === "/") && "Add Cluster") === "Home") || ((state.router.page.path === "/add-cluster") && true)) ? `#F5EFFE` : `transparent`, "color": isTrue((state.router.page.path === "/add cluster") || (((state.router.page.path === "/") && "Add Cluster") === "Home") || ((state.router.page.path === "/add-cluster") && true)) ? `#1A1060` : `black`, "borderRadius": "50%", "boxShadow": "0px 0px 0px 1px rgba(84, 82, 95, 0.14)", "width": "80px", "height": "80px", "padding": "0.9em", "margin": "0.5em"}}>
  <Image src={`/add_cluster.svg`} sx={{"padding": "0.5em"}}/>
</HStack>
</Link>
  <Link as={NextLink} href={`/settings`}>
  <HStack sx={{"bg": isTrue((state.router.page.path === "/settings") || (((state.router.page.path === "/") && "Settings") === "Home") || ((state.router.page.path === "/add-cluster") && false)) ? `#F5EFFE` : `transparent`, "color": isTrue((state.router.page.path === "/settings") || (((state.router.page.path === "/") && "Settings") === "Home") || ((state.router.page.path === "/add-cluster") && false)) ? `#1A1060` : `black`, "borderRadius": "50%", "boxShadow": "0px 0px 0px 1px rgba(84, 82, 95, 0.14)", "width": "80px", "height": "80px", "padding": "0.9em", "margin": "0.5em"}}>
  <Image src={`/settings.svg`} sx={{"padding": "0.5em"}}/>
</HStack>
</Link>
</VStack>
  <Spacer/>
</VStack>
</Box>
  <Box sx={{"paddingTop": "5em", "paddingX": ["auto", "2em"]}}>
  <Box sx={{"width": "100%", "alignItems": "flex-start", "boxShadow": "0px 0px 0px 1px rgba(84, 82, 95, 0.14)", "borderRadius": "0.375rem", "padding": "1em", "marginBottom": "2em"}}>
  <VStack>
  <Heading sx={{"fontSize": "3em"}}>
  {`Add Cluster`}
</Heading>
  <Text>
  {`Welcome to Reflex!`}
</Text>
  <Text>
  {`You can edit this page in `}
  <Code>
  {`{your_app}/pages/add_cluster.py`}
</Code>
</Text>
</VStack>
</Box>
</Box>
  <Spacer/>
  <Box sx={{"position": "fixed", "right": "1.5em", "top": "1.5em", "zIndex": "500"}}>
  <Menu>
  <MenuButton sx={{"width": "3em", "height": "3em", "backgroundColor": "white", "border": "3px solid #F4F3F6", "borderRadius": "0.375rem"}}>
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
  {`Add Cluster`}
</title>
  <meta content={`A Reflex app.`} name={`description`}/>
  <meta content={`/add_cluster.svg`} property={`og:image`}/>
  <meta content={`width=device-width, shrink-to-fit=no, initial-scale=1`} name={`viewport`}/>
</NextHead>
</Fragment>
  )
}
