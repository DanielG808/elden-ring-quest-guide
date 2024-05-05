import { useState } from "react";
import { Dialog } from "@headlessui/react";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";
import { Link } from "react-router-dom";

function Header() {
  // basic use state for mobile menu
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [profileDropdownOpen, setProfileDropdownOpen] = useState(false); // State for profile dropdown

  return (
    <header className="bg-blue border-gold border-b shadow-2xl">
      <nav
        className="flex items-center justify-between -mx-1.5 p-4 lg:px-8"
        aria-label="Global"
      >
        <Link to="/" className="-m-1.5 p-1.5">
          <span className="text-gold font-bold">Elden Ring Quest Tracker</span>
        </Link>
        <div className="flex lg:hidden">
          <button
            type="button"
            className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
            onClick={() => setMobileMenuOpen(true)}
          >
            {/* accessibility for mobile */}
            <span className="sr-only">Open main menu</span>
            <Bars3Icon className="h-6 w-6" aria-hidden="true" />
          </button>
        </div>
        <div className="hidden lg:flex lg:gap-x-12">
          {/* using Link component instead of <a> tags */}
          {/* linking to other pages */}
          <Link
            to="/quests"
            target=""
            className="text-sm font-semibold items-center  leading-6 text-gold"
          >
            Quests
          </Link>
          <Link
            to="/sites-of-grace"
            target=""
            className="text-sm font-semibold items-center leading-6 text-gold"
          >
            Sites Of Grace
          </Link>
          <Link
            to="/items"
            target=""
            className="text-sm font-semibold items-center leading-6 text-gold"
          >
            Items
          </Link>
        </div>
        {/* Profile Dropdown */}
        <div className="relative">
          <button
            onClick={() => setProfileDropdownOpen(!profileDropdownOpen)}
            className="text-sm font-semibold leading-6 text-gold"
          >
            Profile
          </button>
          {profileDropdownOpen && (
            <div className="absolute right-0 mt-5 w-48 bg-white border border-gray-200 rounded-lg shadow-md">
              <Link
                to="/login"
                className="block px-4 py-2 text-gray-800 hover:bg-gray-100"
              >
                Login
              </Link>
              <Link
                to="/signup"
                className="block px-4 py-2 text-gray-800 hover:bg-gray-100"
              >
                Sign Up
              </Link>
            </div>
          )}
        </div>
      </nav>
      {/* Mobile Menu */}
      <Dialog
        as="div"
        className="lg:hidden"
        open={mobileMenuOpen}
        onClose={setMobileMenuOpen}
      >
        <div className="fixed inset-0 z-10" />
        <Dialog.Panel className="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
          <div className="flex items-center justify-between">
            {/* link back to home page */}
            <Link to="/" className="-m-1.5 p-1.5">
              <span className="text-black font-bold">papercuts</span>
            </Link>
            <button
              type="button"
              className="-m-2.5 rounded-md p-2.5 text-gray-700"
              onClick={() => setMobileMenuOpen(false)}
            >
              <span className="sr-only">Close menu</span>
              <XMarkIcon className="h-6 w-6" aria-hidden="true" />
            </button>
          </div>
          <div className="mt-6 flow-root">
            <div className="-my-6 divide-y divide-gray-500/10">
              <div className="space-y-2 py-6">
                <Link
                  target=""
                  to="/"
                  className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gold hover:bg-gray-50"
                >
                  About
                </Link>
                <Link
                  target=""
                  to="/shop"
                  className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gold hover:bg-gray-50"
                >
                  Shop
                </Link>
                <Link
                  target=""
                  to="/"
                  className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gold hover:bg-gray-50"
                >
                  Projects
                </Link>
              </div>
            </div>
          </div>
        </Dialog.Panel>
      </Dialog>
    </header>
  );
}

export default Header;
