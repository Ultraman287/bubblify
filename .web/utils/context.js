import { createContext, useState } from "react"
import { Event, hydrateClientStorage, useEventLoop } from "/utils/state.js"

export const initialState = {"clusters": [], "color_index": 7, "colors": ["#d27cbf", "#d2bf7c", "#7cb3d2", "#7cd2be", "#d27c7c", "#7cd2b3", "#d27cbf", "#7cbfd2"], "diameter_index": 4, "dummy_data": [{"sender": "GitGuardian <security@getgitguardian.com>", "snippet": "GitGuardian has detected the following Google OAuth2 Keys exposed within your GitHub account. Details - Secret type: Google OAuth2 Keys - Repository: Joshtray/bubblify - Pushed date: October 29th 2023,", "subject": "[Joshtray/bubblify] Google OAuth2 Keys exposed on GitHub", "date_received": "2023-10-28", "unread": false, "category_name": "INBOX"}, {"sender": "John Doe <john.doe@example.com>", "snippet": "Hello, just checking in on our project progress. How's it going?", "subject": "Project Progress", "date_received": "2023-10-27", "unread": true, "category_name": "INBOX"}, {"sender": "Alice Smith <alice.smith@example.com>", "snippet": "Meeting reminder for next week. Don't forget to prepare the presentation.", "subject": "Meeting Reminder", "date_received": "2023-10-26", "unread": false, "category_name": "INBOX"}, {"sender": "Support Team <support@example.com>", "snippet": "Your support ticket #12345 has been resolved. If you have any more questions, feel free to ask.", "subject": "Support Ticket Resolution", "date_received": "2023-10-25", "unread": false, "category_name": "INBOX"}, {"sender": "Jane Williams <jane.williams@example.com>", "snippet": "Weekly report attached. Please review and provide feedback.", "subject": "Weekly Report", "date_received": "2023-10-24", "unread": true, "category_name": "INBOX"}, {"sender": "Free Offers <offers@example.com>", "snippet": "Congratulations! You've won a free cruise vacation. Click here to claim your prize!", "subject": "Free Cruise Offer", "date_received": "2023-10-27", "unread": false, "category_name": "Spam"}, {"sender": "Growth Hacks <hacks@example.com>", "snippet": "Get rich quick with our amazing investment opportunity. Don't miss out!", "subject": "Investment Opportunity", "date_received": "2023-10-26", "unread": false, "category_name": "Spam"}, {"sender": "Unsolicited Newsletter <newsletter@example.com>", "snippet": "You're receiving this email because you subscribed to our newsletter. To unsubscribe, click here.", "subject": "Weekly Newsletter", "date_received": "2023-10-25", "unread": false, "category_name": "Spam"}, {"sender": "Amazon Deals <deals@amazon.com>", "snippet": "Check out our latest deals and discounts on electronics, clothing, and more!", "subject": "Amazon Promotions", "date_received": "2023-10-28", "unread": false, "category_name": "Promotions"}, {"sender": "Tech Store <info@techstore.com>", "snippet": "Exclusive offer for tech enthusiasts: 20% off on all gadgets this week only!", "subject": "Tech Store Promotion", "date_received": "2023-10-27", "unread": false, "category_name": "Promotions"}, {"sender": "Fashion Outlet <sales@fashionoutlet.com>", "snippet": "New arrivals and special discounts on fashion items. Shop now!", "subject": "Fashion Outlet Sale", "date_received": "2023-10-26", "unread": false, "category_name": "Promotions"}, {"sender": "Travel Discounts <info@traveldiscounts.com>", "snippet": "Plan your next vacation with our exclusive travel deals and discounts!", "subject": "Travel Discounts", "date_received": "2023-10-25", "unread": false, "category_name": "Promotions"}, {"sender": "Food Delivery <offers@fooddelivery.com>", "snippet": "Get 10% off on your next food delivery order. Use code: DELICIOUS10", "subject": "Food Delivery Discount", "date_received": "2023-10-24", "unread": false, "category_name": "Promotions"}], "index_index": 0, "is_hydrated": false, "messages_index": 3, "name_index": 1, "positionx_index": 5, "positiony_index": 6, "router": {"session": {"client_token": "", "client_ip": "", "session_id": ""}, "headers": {"host": "", "origin": "", "upgrade": "", "connection": "", "pragma": "", "cache_control": "", "user_agent": "", "sec_websocket_version": "", "sec_websocket_key": "", "sec_websocket_extensions": "", "accept_encoding": "", "accept_language": ""}, "page": {"host": "", "path": "", "raw_path": "", "full_path": "", "full_raw_path": "", "params": {}}}, "size_index": 2}

export const ColorModeContext = createContext(null);
export const StateContext = createContext(null);
export const EventLoopContext = createContext(null);
export const clientStorage = {"cookies": {}, "local_storage": {}}

export const initialEvents = () => [
    Event('state.hydrate', hydrateClientStorage(clientStorage)),
]

export const isDevMode = true

export function EventLoopProvider({ children }) {
  const [state, addEvents, connectError] = useEventLoop(
    initialState,
    initialEvents,
    clientStorage,
  )
  return (
    <EventLoopContext.Provider value={[addEvents, connectError]}>
      <StateContext.Provider value={state}>
        {children}
      </StateContext.Provider>
    </EventLoopContext.Provider>
  )
}