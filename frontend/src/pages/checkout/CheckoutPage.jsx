import CheckoutButton from '@/components/CheckoutButton'
import { useToast } from '@/contexts/toastcontext';
import React from 'react'

const CheckoutPage = () => {
    const {showSuccessToast} = useToast()
    const handleSuccess = () => {
        showSuccessToast(`Checkout created successfully`, {
            duration:4000,
            position:'top-right',
        });
      };
  return (
      <div className="flex flex-col items-center gap-1 text-center px-24 py-24">
        <CheckoutButton onSuccess={handleSuccess} />
      </div>
    
  )
}

export default CheckoutPage