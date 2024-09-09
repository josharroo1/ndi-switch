import tkinter as tk
import asyncio
from ndi_decoder_control import NDIDecoderControl

async def main():
    root = tk.Tk()
    app = NDIDecoderControl(root)
    
    # Run the login method
    try:
        login_success = await app.login()
        if not login_success:
            print("Login failed. Exiting...")
            await safe_cleanup(app)
            root.quit()
            return
    except Exception as e:
        print(f"An error occurred during login: {e}")
        await safe_cleanup(app)
        root.quit()
        return
    
    # Start tkinter main loop in the main thread
    root.after(100, lambda: asyncio.create_task(run_async_tasks(app)))
    root.protocol("WM_DELETE_WINDOW", lambda: asyncio.create_task(on_closing(root, app)))
    root.mainloop()async def run_async_tasks(app):
    while True:
        # Perform any async tasks here
        await asyncio.sleep(0.1)

async def safe_cleanup(app):
    try:
        await app.cleanup()
    except Exception as e:
        print(f"Error during cleanup: {e}")

async def on_closing(root, app):
    await safe_cleanup(app)
    root.quit()

if __name__ == "__main__":
    asyncio.run(main())

